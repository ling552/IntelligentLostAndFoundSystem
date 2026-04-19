import sys

print('python_executable:', sys.executable)
print('python_version:', sys.version)

try:
    import django

    print('django_version:', django.get_version())
except Exception as e:
    print('django_import_error:', repr(e))

try:
    import os

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound_system.settings')
    from django.core.management import execute_from_command_line

    execute_from_command_line(['manage.py', 'check', '-v', '2'])
except Exception as e:
    print('django_manage_check_error:', repr(e))
    raise
