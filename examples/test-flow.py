from zag import PyTask, ShellTask, Stage, Sequence

bar = PyTask(
    path="$PATH/foo/bar.py",
    entrypoint="main",
    parser="build_parser")

shell = ShellTask(
    script="ls -al")

workflows = [
    Sequence("main", stages=[
        Stage("print-date",
            bar,
            args=[
                ("--date",)
            ],
            tags=["date"]),

        Stage("list-dir",
            shell,
            args=[
                ("$PATH/$list_path", )
            ],
            tags=["list-dir"])
    ])
]

