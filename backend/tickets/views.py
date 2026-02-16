from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Ticket, Member
from .serializers import TicketSerializer
from django.db.models import Count, Q

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        # 1. Get the issue type from the submitted form
        issue_type = self.request.data.get('issue_type')
        
        # 2. Find the best member (The Brain/Active Load Logic)
        # We look for members with matching specialty, ordered by 
        # count of 'OPEN' or 'ASSIGNED' tickets
        best_member = Member.objects.filter(
            specialty=issue_type, 
            is_active=True
        ).annotate(
            active_load=Count('ticket', filter=Q(ticket__status__in=['OPEN', 'ASSIGNED']))
        ).order_by('active_load').first()

        # 3. Save the ticket with the assigned member
        if best_member:
            serializer.save(assigned_member=best_member, status='ASSIGNED')
        else:
            serializer.save(status='OPEN') # No member found, leave it unassigned
# Create your views here.
