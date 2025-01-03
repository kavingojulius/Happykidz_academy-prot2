from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Message
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth import get_user_model
from .models import *
from main.models import StudentAdmission
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from main.models import StudentAdmission
from django.db.models import Sum, F
from django.db.models.functions import ExtractYear
from collections import defaultdict
import io


# get_user_model() fetches the custom user model
User = get_user_model()  # This will now refer to 'portal.CustomUser'

@login_required
def portal(request):
    admin_user = User.objects.get(is_superuser=True)  # Assuming admin is the superuser
    messages = Message.objects.filter(sender=request.user, receiver=admin_user) | \
               Message.objects.filter(sender=admin_user, receiver=request.user)
    messages = messages.order_by('timestamp')

    # Get unread messages count
    unread_count = Message.objects.filter(receiver=request.user,sender=request.user, read=False).count()
    
    # Mark unread messages as read when the admin opens the chat
    Message.objects.filter(sender=request.user, receiver=request.user, read=False).update(read=True)

 # Get the current user's reg_number
    reg_number = request.user.reg_number

    # Filter the students based on the reg_number
    students = StudentDet.objects.filter(reg_number=reg_number)


# Get the student with the matching reg_number (assuming unique reg_number)
    try:
        student = StudentDet.objects.get(reg_number=reg_number)
    except StudentDet.DoesNotExist:
        student = None

    results_data = []
    if student:
        # Get results grouped by term and term section
        results = Results.objects.filter(student=student).select_related('term', 'term_section', 'subject')
        grouped_results = {}
        for term in results.values_list('term__term', flat=True).distinct():
            term_results = results.filter(term__term=term)
            grouped_results[term] = {}
            for section in term_results.values_list('term_section__term_section', flat=True).distinct():
                section_results = term_results.filter(term_section__term_section=section)
                total_marks = section_results.aggregate(total=Sum('marks'))['total']
                grouped_results[term][section] = {
                    'results': section_results,
                    'total_marks': total_marks,
                }

        results_data = grouped_results

    # Group fees by term and year
    fee_data = {}
    if student:
        # Group fees by term and year
        fees = PayFee.objects.filter(student=student).annotate(year=F('date_paid'))

        for fee in fees:
            key = f"{fee.term.term} - {fee.year}"
            if key not in fee_data:
                fee_data[key] = {
                    'term': fee.term.term,
                    'year': fee.year,
                    'transactions': [],
                    'total_amount': 0,
                    'balance': 0  # Initialize balance
                }
            fee_data[key]['transactions'].append(fee)
            fee_data[key]['total_amount'] += fee.amount or 0
        
        # Now calculate the balance for each term-year based on the TermFee model
        for key, data in fee_data.items():
            # Get the fee for this term and year
            try:
                term_fee = TermFee.objects.get(term__term=data['term'], year=data['year'], class_level=student.class_level)
                total_term_fee = term_fee.fee
            except TermFee.DoesNotExist:
                total_term_fee = 0

            # Calculate the balance
            data['balance'] = total_term_fee - data['total_amount']

    transactions = PayFee.objects.filter(student=student)
    total_amount = sum(transaction.amount for transaction in transactions)    
    health_records = HealthProgress.objects.filter(student__in=students)

    if request.method == 'POST':
        message_text = request.POST['message']
        if message_text:
            Message.objects.create(sender=request.user, receiver=admin_user, message=message_text)
            return redirect('portal')  # Reload the page after submitting

    return render(request, 'portal/portal.html', {
        'messages': messages,
        'unread_count': unread_count,  # Pass unread count to the template
        'students': students,
        'transactions': transactions,
        'total_amount': total_amount,
        'health_records': health_records,
        'results_data': results_data,
        'fee_data': fee_data,  # Pass grouped fee data to the template
    })

@login_required
def admin(request):
    # Retrieve all student admission records
    admissions = StudentAdmission.objects.all().order_by('-submitted_at')  # Order by submission time, latest first
    return render(request, 'portal/admin.html', {'admissions': admissions})

def download_admissions_pdf(request):
    # Create a byte stream buffer to hold the PDF
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    # Define the header
    styles = getSampleStyleSheet()
    header = Paragraph("Admission Requests Report", styles['Title'])
    subheader = Paragraph("List of all admission requests submitted by prospective students.", styles['BodyText'])
    elements.extend([header, subheader])

    # Define the table data
    admissions = StudentAdmission.objects.all()
    data = [["#", "Name", "Gender", "D.O.B", "Class Applied", "Parent Name", "Contact", "Submitted At"]]
    
    for i, admission in enumerate(admissions, start=1):
        row = [
            i,
            f"{admission.first_name} {admission.last_name}",
            admission.gender,
            admission.date_of_birth.strftime("%Y-%m-%d"),
            admission.applying_class,
            f"{admission.parent_first_name} {admission.parent_last_name}",
            admission.parent_phone,
            admission.submitted_at.strftime("%Y-%m-%d %H:%M:%S"),
        ]
        data.append(row)

    # Create table and set style
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    pdf.build(elements)

    # Return the PDF as an HTTP response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="admission_requests.pdf"'
    return response

@login_required
def delete_chats(request):
    if request.method == 'POST':
        admin_user = User.objects.get(is_superuser=True)
        # Delete all messages between the user and the admin
        Message.objects.filter(sender=request.user, receiver=admin_user).delete()
        Message.objects.filter(sender=admin_user, receiver=request.user).delete()
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=403)

def log_in(request):        
    if request.method == 'POST':        
        # email=request.POST.get('email')
        username=request.POST.get('username')
        pass1=request.POST.get('password1')        

        user=authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request,user)
            # Check if the user is a superuser
            if user.is_superuser:
                return redirect('admin')  # Redirect to the admin page if superuser
            else:
                return redirect('portal')  # Redirect to the portal page for other users
        else:
            return redirect('log_in')
        
    return render(request, 'portal/log_in.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('portal')  # Redirect back to the portal after success
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'portal/change_password.html', {'form': form})

@login_required
def admin_conversations(request):
    if not request.user.is_superuser:
        return redirect('home')

    # Get users who have sent messages to the admin
    users = User.objects.filter(sent_messages__receiver=request.user).distinct()

    users_with_unread = {}
    for user in users:
        unread_count = Message.objects.filter(sender=user, receiver=request.user, read=False).count()
        users_with_unread[user.id] = unread_count

    # If it's an AJAX request, return the list of users and their unread counts
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'users': list(users.values()),
            'users_with_unread': users_with_unread
        })

    return render(request, 'portal/admin_conversations.html', {
        'users': users,
        'users_with_unread': users_with_unread,
    })

@csrf_exempt
@login_required
def delete_conversation(request):
    if request.method == 'POST' and request.user.is_superuser:
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        # Assuming Message is the model for chat messages
        Message.objects.filter(sender=user, receiver=request.user).delete()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=403)

def check_new_users(request):
    """Function to check for new users who have sent messages."""
    if request.user.is_superuser:
        new_users = User.objects.filter(sent_messages__receiver=request.user).exclude(id__in=users)
        new_users_list = [{'id': user.id, 'username': user.username} for user in new_users]
        return JsonResponse({'new_users': new_users_list})
    return JsonResponse({'new_users': []})

@login_required
def admin_chat(request, user_id):
    if not request.user.is_superuser:
        return redirect('home')  # Restrict access to admin

    user = User.objects.get(id=user_id)
    admin_user = request.user

    # Fetch all messages between the admin and the user
    messages = Message.objects.filter(sender=user, receiver=admin_user) | \
               Message.objects.filter(sender=admin_user, receiver=user)
    messages = messages.order_by('timestamp')

    # Mark unread messages as read when the admin opens the chat
    Message.objects.filter(sender=user, receiver=admin_user, read=False).update(read=True)

    if request.method == 'POST':
        message_text = request.POST['message']
        if message_text:
            Message.objects.create(sender=admin_user, receiver=user, message=message_text)
            return redirect('admin_chat', user_id=user.id)

    return render(request, 'portal/admin_chat.html', {'messages': messages, 'user': user})

@login_required
def get_messages(request, user_id=None):
    admin_user = request.user if request.user.is_superuser else User.objects.get(is_superuser=True)
    user = User.objects.get(id=user_id) if user_id else request.user

    messages = Message.objects.filter(sender=user, receiver=admin_user) | \
               Message.objects.filter(sender=admin_user, receiver=user)
    messages = messages.order_by('timestamp')

    # Mark all unread messages from admin as read when user opens the chat
    if not request.user.is_superuser:
        Message.objects.filter(sender=admin_user, receiver=user, read=False).update(read=True)

    # Convert the queryset to JSON
    messages_json = serializers.serialize('json', messages)
    return JsonResponse({'messages': messages_json})















