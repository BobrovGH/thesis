from django.contrib import admin
from .models import Author, Genre, Text, TextEditionHistory

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_birth', 'date_death')

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

class TextAdmin(admin.ModelAdmin):
    list_display = ('title', 'text_type', 'display_authors', 'display_genres', 'source', 'year', 'pages', 'time_to_read', 'level', 'language', 'description')
    #при сохранении создаётся первая история редактирования 
    def save_model(self, request, obj, form, change):
        # Save the Text object
        super().save_model(request, obj, form, change)

        # Create a TextEditionHistory object
        TextEditionHistory.objects.create(
            user=request.user,
            text=obj,
            comment="Объект создан"
        )
        
    #так как авторы и жанры это поля много ко многим, необходимо добавить функции для их отображения в интерфейсе администратора 
    def display_authors(self, obj):
        return ", ".join([author.name for author in obj.authors.all()])

    display_authors.short_description = 'Authors'

    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    display_genres.short_description = 'Genres'

class TextEditionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'edited_on')

# Register your models with the custom ModelAdmin subclasses
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(TextEditionHistory, TextEditionHistoryAdmin)
