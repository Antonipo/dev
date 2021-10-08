{
    'name': 'Universidad Gerencia',
    'depends': ['base'],
    'category': 'universidad',
    'data': [
            'views/course_college.xml',
            'views/teacher_college.xml',
            'views/college_student.xml',
            'views/hello_world.xml',
            'security/groups.xml',
            'security/ir.model.access.csv',
            'views/teacher_assets.xml',
             ],
    'qweb': [
            'static/src/xml/hello_world.xml',
        ]


 }