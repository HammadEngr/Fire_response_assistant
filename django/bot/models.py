from django.db import models

class FireCategory(models.Model):
    """
    Main fire categories: House, Building, Factory, Warehouse, Forest
    """
    name = models.CharField(
        max_length=50, 
        unique=True,
        help_text="Internal name (e.g., 'house', 'building')"
    )
    display_name = models.CharField(
        max_length=100,
        help_text="Display name (e.g., 'House Fire', 'Building Fire')"
    )
    icon = models.CharField(
        max_length=10, 
        blank=True, 
        null=True,
        help_text="Emoji icon (e.g., '🏠', '🏢')"
    )
    description = models.TextField(
        blank=True, 
        null=True,
        help_text="Optional description of this category"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order in menus"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this category is active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fire_categories'
        verbose_name = 'Fire Category'
        verbose_name_plural = 'Fire Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.icon} {self.display_name}" if self.icon else self.display_name


class SubCategory(models.Model):
    """
    Sub-categories within each fire category
    e.g., House -> Kitchen, Electrical, Bedroom, etc.
    """
    category = models.ForeignKey(
        FireCategory,
        on_delete=models.CASCADE,
        related_name='sub_categories'
    )
    name = models.CharField(
        max_length=50,
        help_text="Internal name (e.g., 'kitchen', 'electrical')"
    )
    display_name = models.CharField(
        max_length=100,
        help_text="Display name (e.g., 'Kitchen Fire', 'Electrical Fire')"
    )
    icon = models.CharField(
        max_length=10, 
        blank=True, 
        null=True,
        help_text="Emoji icon (e.g., '🍳', '⚡')"
    )
    description = models.TextField(
        blank=True, 
        null=True,
        help_text="Optional description"
    )
    has_risk_levels = models.BooleanField(
        default=True,
        help_text="Whether this sub-category uses risk levels"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order within category"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this sub-category is active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sub_categories'
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'
        ordering = ['category', 'order', 'name']
        unique_together = ['category', 'name']

    def __str__(self):
        icon = self.icon or self.category.icon or ''
        return f"{icon} {self.category.display_name} → {self.display_name}"


class RiskLevel(models.Model):
    """
    Risk levels: Critical, High, Rising, Low
    """
    name = models.CharField(
        max_length=50, 
        unique=True,
        help_text="Internal name (e.g., 'critical', 'high')"
    )
    display_name = models.CharField(
        max_length=100,
        help_text="Display name (e.g., 'Critical', 'High Risk')"
    )
    icon = models.CharField(
        max_length=10,
        help_text="Emoji icon (e.g., '🚨', '🟠')"
    )
    color = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text="CSS color (e.g., 'red', '#FF0000')"
    )
    severity = models.PositiveIntegerField(
        default=0,
        help_text="Severity order (1=highest, 4=lowest)"
    )
    description = models.TextField(
        blank=True, 
        null=True,
        help_text="Description of this risk level"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this risk level is active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'risk_levels'
        verbose_name = 'Risk Level'
        verbose_name_plural = 'Risk Levels'
        ordering = ['severity']

    def __str__(self):
        return f"{self.icon} {self.display_name}"


class FireResponse(models.Model):
    """
    Main response content table
    Links category + sub_category + risk_level to actual response content
    """
    # Relationships
    category = models.ForeignKey(
        FireCategory,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    sub_category = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='responses',
        blank=True,
        null=True,
        help_text="Optional sub-category"
    )
    risk_level = models.ForeignKey(
        RiskLevel,
        on_delete=models.CASCADE,
        related_name='responses',
        blank=True,
        null=True,
        help_text="Optional risk level"
    )
    
    # Unique key for lookup
    response_key = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique lookup key (e.g., 'house_kitchen_critical')"
    )
    
    # Content
    title = models.CharField(
        max_length=200,
        help_text="Response title/header"
    )
    content = models.TextField(
        help_text="Main response content"
    )
    additional_warning = models.TextField(
        blank=True,
        null=True,
        help_text="Additional context-specific warning"
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this response is active"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fire_responses'
        verbose_name = 'Fire Response'
        verbose_name_plural = 'Fire Responses'
        ordering = ['category', 'sub_category', 'risk_level']
        indexes = [
            models.Index(fields=['response_key']),
            models.Index(fields=['category', 'sub_category', 'risk_level']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        parts = [self.category.display_name]
        if self.sub_category:
            parts.append(self.sub_category.display_name)
        if self.risk_level:
            parts.append(f"({self.risk_level.display_name})")
        return " → ".join(parts)

    def save(self, *args, **kwargs):
        # Auto-generate response_key if not set
        if not self.response_key:
            self.response_key = self.generate_response_key()
        super().save(*args, **kwargs)

    def generate_response_key(self):
        """Generate response key from category, sub_category, and risk_level"""
        parts = [self.category.name]
        if self.sub_category:
            parts.append(self.sub_category.name)
        if self.risk_level:
            parts.append(self.risk_level.name)
        return "_".join(parts)

    def get_full_response(self):
        """Return complete response with additional warning if present"""
        response = self.content
        if self.additional_warning:
            response += f"\n\n{self.additional_warning}"
        return response

    @classmethod
    def get_by_key(cls, response_key):
        """Fetch active response by key"""
        try:
            return cls.objects.get(response_key=response_key, is_active=True)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_response_content(cls, category, sub_category=None, risk_level=None):
        """Fetch response by category, sub_category, and risk_level names"""
        try:
            query = cls.objects.filter(
                category__name=category,
                is_active=True
            )
            
            if sub_category:
                query = query.filter(sub_category__name=sub_category)
            else:
                query = query.filter(sub_category__isnull=True)
            
            if risk_level:
                query = query.filter(risk_level__name=risk_level)
            else:
                query = query.filter(risk_level__isnull=True)
            
            response = query.first()
            return response.get_full_response() if response else None
        except Exception:
            return None