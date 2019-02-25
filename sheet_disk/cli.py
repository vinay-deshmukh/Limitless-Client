'''Wrapper file around the main function 
in sheet_disk, so module can be called from Command Line Interface'''

from .sheet_disk import main

if __name__ == '__main__':
    raise RuntimeError(
        'dont use cli interface, directly call'
        ' sheet_disk.sheet_disk.main() '
        ' with oauth_json_string '
        )
    main()
