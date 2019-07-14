x = [1, 2, 3]
f = lambda x: x

def func(
        no_defaults,
        empty_list=[],
        nonempty_list=[1,2,],
        empty_dict={},
        nonempty_dict={'a': 2},
        empty_set=set(),
        nonempty_set=set(1, 2),
        variable=x,
        call=f(x),
        empty_tuple=tuple(),
        nonempty_tuple=(1, 2),
        listcomp=[elem for elem in x],
        dictcomp={elem: elem for elem in x},
        setcomp={elem for elem in x},
        generator=(elem for elem in x),
    ):
    pass