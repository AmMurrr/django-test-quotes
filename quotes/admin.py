from django.contrib import admin
from .models import Quote, PageView, Comment, Rating
from django.urls import path
from django.shortcuts import render, redirect
from django.db.models import Count
import json

# кастомная админка для дашбордов
class MyAdminSite(admin.AdminSite):
    site_header = ' Цитатник Админка'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboards/', self.admin_view(self.dashboards_view), name='dashboards'),
        ]
        return custom_urls + urls

    def dashboards_view(self, request):
        # Получаем данные для графика
        rating_data = (
            Rating.objects.values('score')
            .annotate(count=Count('score'))
            .order_by('score')
        )

        # Готовим данные для  дашборда
        labels = [item['score'] for item in rating_data]
        data = [item['count'] for item in rating_data]

        # Полный набор меток от 1 до 5
        full_labels = list(range(1, 6))
        full_data = [0] * 5
        for i, label in enumerate(labels):
            if 1 <= label <= 5:
                full_data[label - 1] = data[i]

        # данные по просмотрам страниц
        page_views_qs = PageView.objects.all().order_by('name')
        page_view_labels = [pv.name for pv in page_views_qs]
        page_view_counts = [pv.views for pv in page_views_qs]

        context = dict(
            self.each_context(request),
            rating_labels=json.dumps(full_labels),
            rating_data=json.dumps(full_data),
            page_view_labels=json.dumps(page_view_labels),
            page_view_data=json.dumps(page_view_counts),
        )
        return render(request, "admin/dashboards.html", context)  

admin_site = MyAdminSite(name='myadmin')

# Прокси-модель для отображения ссылки на дэшборд 
class Dashboard(Rating):
    class Meta:
        proxy = True
        verbose_name = 'Dashboard'

class DashboardAdmin(admin.ModelAdmin):
    def changelist_view(self, request):
        return redirect('admin:dashboards')


# Регаем модели в нашей админке
admin_site.register(Quote)
admin_site.register(PageView)
admin_site.register(Comment)
admin_site.register(Rating)
admin_site.register(Dashboard, DashboardAdmin)
