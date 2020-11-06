import os
import shutil


def make_archive(source, destination):
    """Funktion zum Erstellen von zip-Archiven.

    Wrapper für shutil.make_archive, um die Benutzung zu erleichtern.
    Vgl. http://www.seanbehan.com/how-to-use-python-shutil-make_archive-to-zip-up-a-directory-recursively-including-the-root-folder/
    """
    archive_base = os.path.basename(destination)
    archive_name = archive_base.split('.')[0]
    archive_format = archive_base.split('.')[1]
    archive_from = os.path.dirname(source)
    archive_to = os.path.basename(source.strip(os.sep))
    shutil.make_archive(archive_name, archive_format, archive_from, archive_to)
    shutil.move('%s.%s' % (archive_name, archive_format), destination)