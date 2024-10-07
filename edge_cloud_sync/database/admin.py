
from django.contrib import admin
from .models import Event, MediaFile

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'source_id', 'status', 'retry_count', 'created_at', 'updated_at')
    search_fields = ('event_id', 'source_id', 'status')
    list_filter = ('status', 'source_id', 'created_at', 'retry_count')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'retry_count', 'status')

    fieldsets = (
        ('Event Information', {
            'fields': ('event_id', 'source_id', 'data', 'status', 'retry_count', 'error_message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    class MediaFileInline(admin.TabularInline):
        model = MediaFile
        extra = 0

    # Add the media file inline to display linked media files
    inlines = [MediaFileInline]
    
    
@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('event', 'file_path', 'uploaded')
    list_filter = ('uploaded', )