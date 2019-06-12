import os
import tkinter as tk
from tkinter import N, S, E, W
from covers import process_album


def process_one(album_path, candidate_frame, echo):
    p = process_album(album_path)
    for status, *args in p:
        if 'candidates' in status:
            echo.set('%s has candidates.' % args[0])
            yield args[1]
        else:
            echo.set('%s: %s' % (args[0], status))


def lets_go(echo, candidate_frame, root_path):
    def f():
        root_path_ = root_path.get()
        for d in os.listdir(root_path_):
            for y in process_one(os.path.join(root_path_, d), candidate_frame, echo):
                tk.Button(candidate_frame, text='Nin!', command=lambda: next(p)).pack()

    return f


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Good morning or die')

    main = tk.Frame(root)

    root_path_str = tk.StringVar()
    root_path_str.set('D:\\fuck163music')
    root_path_entry = tk.Entry(main, width=30, textvariable=root_path_str)

    echo_str = tk.StringVar()
    echo_str.set('Standby.')
    current_path = tk.Label(main, textvariable=echo_str)

    candidate_frame = tk.Frame(main)

    lets_go_button = tk.Button(main, text="Let's go!", command=lets_go(echo_str, candidate_frame, root_path_str))

    main.grid(column=0, row=0, sticky=(N, S, E, W))
    root_path_entry.grid(column=0, row=0, columnspan=4, rowspan=1, sticky=(N, W))
    lets_go_button.grid(column=4, row=0, sticky=(E, N))
    current_path.grid(column=0, row=1, columnspan=5, rowspan=1, sticky=(W, E))
    candidate_frame.grid(column=0, row=2, columnspan= 5, rowspan=10, sticky=(E, W, S))

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    for i in range(5):
        main.columnconfigure(i, weight=1)
        main.rowconfigure(i, weight=1)

    root.mainloop()
