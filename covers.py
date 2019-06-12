import functools
import os
import mutagen
import tkinter as tk
from PIL import ImageTk, Image


def consists(method):
    return lambda text: lambda *keywords: any(map(lambda k: method(text, k), keywords))


def has_extension(fn):
    return consists(lambda text, kw: text.endswith(kw))(fn)


def is_music_file(fn):
    return has_extension(fn)('.mp3')


def is_image_file(fn):
    return has_extension(fn)('.jpg', '.png')


def is_album_art(fn):
    return is_image_file(fn) and consists(lambda f, kw: f.startswith(kw))(fn)('cover', 'front')


def has_embedded_album_art(fp):
    try:
        f = mutagen.File(fp)
        artwork = f.tags.getall('APIC')
        return bool(artwork)
    except Exception as e:
        print(fp)
        print(e)


def process_root(root_folder):
    for album_path in os.listdir(root_folder):
        yield album_path, functools.partial(process_album, os.path.join(root_folder, album_path))


dummy = lambda *a, **k: a


def process_album(folder_path, not_album_folder=dummy, album_art_ok=dummy, album_art_has_candidates=dummy, yield_=True):
    image_files = []

    for dir_path, dir_names, file_names in os.walk(folder_path):
        image_files.extend(os.path.join(dir_path, fn) for fn in file_names if is_image_file(fn))

        if any(map(is_music_file, file_names)):
            if any(map(is_album_art, file_names)):
                album_art_ok(dir_path)
                if yield_:
                    yield 'album art ok', dir_path
            elif any(map(lambda fn: has_embedded_album_art(os.path.join(dir_path, fn)), filter(is_music_file, file_names))):
                album_art_ok(dir_path, embedded=True)
                if yield_:
                    yield 'album art ok (embedded)', dir_path
            else:
                album_art_has_candidates(dir_path, image_files)
                if yield_:
                    yield 'album art has candidates', dir_path, image_files
        else:
            not_album_folder(dir_path)
            if yield_:
                yield 'not album folder', dir_path


class ArtworkArray(tk.Frame):
    def __init__(self, artworks, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.artwork_objs = {f: ImageTk.PhotoImage(Image.open(f)) for f in artworks}
        self.selected = None
        self.create_array()
        self.pack()

    def create_array(self):
        def create_button(f, img):
            def callback():
                self.selected = f
            tk.Button(self, image=img, command=callback).pack()

        self.buttons = map(lambda x: create_button(*x), self.artwork_objs.items())


if __name__ == '__main__':
    def result_accumulated(accumulator):
        def wrapper(func):
            @functools.wraps(func)
            def f(*args, **kwargs):
                accumulator.append(func(*args, **kwargs))
            return f
        return wrapper

    not_album_acc = []
    @result_accumulated(accumulator=not_album_acc)
    def not_album_folder(p):
        return p

    candidates_raw = []
    @result_accumulated(accumulator=candidates_raw)
    def album_art_has_candidates(*k):
        return k

    has_album_acc = []
    @result_accumulated(accumulator=has_album_acc)
    def has_album(k, embedded=False):
        return '%s embedded' % k if embedded else k

    entry = r'D:/fuck163music'
    for d in os.listdir(entry):
        process_album(os.path.join(entry, d), not_album_folder, has_album, album_art_has_candidates)

    print('Not an album folder')
    for k in not_album_acc:
        print(k)
    print()
    print('Candidates')
    for k, v in dict(candidates_raw).items():
        print(k, v)
        try:
            if not v:
                continue
            ArtworkArray(v).mainloop()
        except Exception as e:
            print(e)
    print()
    print('OK')
    for k in has_album_acc:
        print(k)
