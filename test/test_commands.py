from analyzer.parser import parser
from pytest import mark

test_cases = [
    'Configure -type->local -encrypt_log->false -encrypt_read->false',
    'rEnAme -pAth->/carpeta1/prueba1.txt -name->b1.txt',
    'create -name->"prueba 2.txt" -path->"/carpeta 2/" -body->"Este es el contenido del archivo 2"',
    'delete -path->/carpeta1/ -name->prueba1.txt',
    'delete -path->"/carpeta 2/"',
    'Copy -from->/carpeta1/prueba1.txt -to->"/carpeta 2/"',
    'Copy -from->"/carpeta 2/" -to->/carpeta1/',
    'transfer -from->/carpeta1/prueba1.txt -to->"/carpeta 2/" -mode->"local"',
    'transfer -from->"/carpeta 2/" -to->/carpeta1/ -mode->"cloud"',
    'rename -path->/carpeta1/prueba1.txt -name->b1.txt',
    'rename -path->/carpeta1/prueba1.txt -name->b1.txt',
    'modify -path->/carpeta1/prueba1.txt -body->" este es el nuevo contenido del archivo"',
    'add -path->/carpeta1/prueba1.txt -body->" este es el nuevo contenido del archivo"',
    'backup',
    'exec -path->/home/Desktop/calificacion.mia'
]


@mark.parametrize(
    'test_case, expected',
    [
        x for x in zip(test_cases, [
            ('configure', {'type': 'local',
             'encrypt_log': 'false', 'encrypt_read': 'false'}),
            ('rename', {'path': '/carpeta1/prueba1.txt', 'name': 'b1.txt'}),
            ('create', {'name': 'prueba 2.txt', 'path': '/carpeta 2/',
             'body': 'Este es el contenido del archivo 2'}),
            ('delete', {'path': '/carpeta1/', 'name': 'prueba1.txt'}),
            ('delete', {'path': '/carpeta 2/'}),
            ('copy', {'from': '/carpeta1/prueba1.txt', 'to': '/carpeta 2/'}),
            ('copy', {'from': '/carpeta 2/', 'to': '/carpeta1/'}),
            ('transfer', {'from': '/carpeta1/prueba1.txt',
             'to': '/carpeta 2/', 'mode': 'local'}),
            ('transfer', {'from': '/carpeta 2/',
             'to': '/carpeta1/', 'mode': 'cloud'}),
            ('rename', {'path': '/carpeta1/prueba1.txt', 'name': 'b1.txt'}),
            ('rename', {'path': '/carpeta1/prueba1.txt', 'name': 'b1.txt'}),
            ('modify', {'path': '/carpeta1/prueba1.txt',
             'body': ' este es el nuevo contenido del archivo'}),
            ('add', {'path': '/carpeta1/prueba1.txt',
             'body': ' este es el nuevo contenido del archivo'}),
            ('backup', {}),
            ('exec', {'path': '/home/Desktop/calificacion.mia'})
        ])
    ]
)
def test_parser(test_case, expected):
    param_name, params = parser.parse(test_case)
    assert param_name == expected[0]
    assert params == expected[1]
