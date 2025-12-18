{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'estate',
    'description': """
    Real Estate Property
    """,
    'depends': [
        'base',
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml', 
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/res_users_form.xml'
    ],
    'installable': True,
    'application': True,

}