def test():
    from render import render, Model

    render(Model("res/monkey.obj"), height=4020, width=4020, filename="monkey.png")


if __name__ == "__main__":
    test()
