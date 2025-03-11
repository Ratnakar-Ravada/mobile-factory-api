from pydantic import BaseModel, field_validator
from typing import List

class Component(BaseModel):
    code: str
    price: float
    name: str
    category: str

# Store components data in memory
COMPONENTS = {
    'A': Component(code='A', price=10.28, name='LED Screen', category='Screen'),
    'B': Component(code='B', price=24.07, name='OLED Screen', category='Screen'),
    'C': Component(code='C', price=33.30, name='AMOLED Screen', category='Screen'),
    'D': Component(code='D', price=25.94, name='Wide-Angle Camera', category='Camera'),
    'E': Component(code='E', price=32.39, name='Ultra-Wide-Angle Camera', category='Camera'),
    'F': Component(code='F', price=18.77, name='USB-C Port', category='Port'),
    'G': Component(code='G', price=15.13, name='Micro-USB Port', category='Port'),
    'H': Component(code='H', price=20.00, name='Lightning Port', category='Port'),
    'I': Component(code='I', price=42.31, name='Android OS', category='OS'),
    'J': Component(code='J', price=45.00, name='iOS OS', category='OS'),
    'K': Component(code='K', price=45.00, name='Metallic Body', category='Body'),
    'L': Component(code='L', price=30.00, name='Plastic Body', category='Body')
}

REQUIRED_CATEGORIES = {'Screen', 'Camera', 'Port', 'OS', 'Body'}

class OrderSerializer(BaseModel):
    components: List[str]

    @field_validator('components', mode='before')
    def validate_components(cls, v):
        """Validate the components list."""
        if not isinstance(v, list):
            raise Exception("'Components' must be a list.")

        codes = set()
        duplicates = []
        for code in v:
            if code in codes:
                duplicates.append(code)
            else:
                codes.add(code)
        if len(duplicates) > 0:
            raise Exception(f"Duplicate component codes found: '{', '.join(duplicates)}'")

        selected_categories = {}
        for code in v:
            if code not in COMPONENTS:
                raise Exception(f"Invalid component code: '{code}'")

            category = COMPONENTS[code].category
            if category in selected_categories:
                raise Exception(f"Duplicate component for category: '{category}'")
            selected_categories[category] = code

        missing_categories = REQUIRED_CATEGORIES - set(selected_categories.keys())
        if missing_categories:
            raise Exception(f"Missing components for categories: '{', '.join(missing_categories)}'")

        return v