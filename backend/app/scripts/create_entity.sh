cp app/models/item.py app/models/portfolio.py
cp app/crud/crud_item.py app/crud/crud_portfolio.py
cp app/schemas/item.py app/schemas/portfolio.py
cp app/api/api_v1/endpoints/items.py app/api/api_v1/endpoints/portfolios.py
# modify app/db/base.py to add model 
# modify crud/__init__.py to add cruds
# modify models/__init__.py to add model
# modify schema/__init__.py to add supported schemas