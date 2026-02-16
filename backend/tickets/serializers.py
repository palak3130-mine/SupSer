from rest_framework import serializers
from .models import Ticket, Member

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'org_name', 'issue_type', 'description', 'contact_info', 'status', 'assigned_member', 'created_at']
        read_only_fields = ['status', 'assigned_member'] # The logic handles these, not the user