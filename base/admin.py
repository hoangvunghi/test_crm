from django.contrib import admin
from .models import Customer, Employee, Product, Task

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'is_active')  
    search_fields = ('user__username', 'phone', 'address')    
    list_filter = ('is_active',)                              

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'position', 'is_active')
    search_fields = ('user__username', 'phone', 'address', 'position')
    list_filter = ('is_active', 'position')  

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at', 'updated_at')
    search_fields = ('name', 'description')  
    list_filter = ('created_at', 'updated_at')  

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'assigned_to', 'due_date', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'assigned_to__user__username')  
    list_filter = ('status', 'assigned_to', 'due_date')  