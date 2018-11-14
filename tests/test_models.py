from ftree.models import FileTree


def test_load(tmpdir):
    t = tmpdir.mkdir('sub').join('tests.py')
    t.write('import pytest\n')
    m = tmpdir.join('main.py')
    m.write('import this\n')

    ft = FileTree.load(tmpdir.strpath)
    assert ft.name == ''
    assert not ft.read_only
    assert ft.is_dir
    assert len(ft.children) == 2

    main = ft.children[0]
    assert main.name == 'main.py'
    assert main.content == 'import this\n'
    assert not main.read_only
    assert not main.binary
    assert not main.too_big
    assert main.changed

    assert ft.children[1].name == 'sub'
    assert ft.children[1].is_dir
    assert len(ft.children[1].children) == 1

    testfile = ft.children[1].children[0]
    assert testfile.name == 'tests.py'
    assert testfile.content == 'import pytest\n'
    assert not testfile.read_only
    assert not testfile.binary
    assert not testfile.too_big
    assert testfile.changed


def test_load_binary(tmpdir):
    b = tmpdir.join('binary.db')
    b.write_binary(b'\xe6')

    ft = FileTree.load(tmpdir.strpath)
    assert ft.name == ''
    assert len(ft.children) == 1

    bf = ft.children[0]
    assert bf.name == 'binary.db'
    assert bf.content == '5g=='
    assert bf.binary


def test_load_readonly(tmpdir):
    r = tmpdir.join('readonly.py')
    r.write('import pytest')
    import stat
    r.chmod(stat.S_IRUSR)
    try:
        ft = FileTree.load(tmpdir.strpath)
        rf = ft.children[0]
        assert rf.read_only
    finally:
        r.chmod(stat.S_IRWXU)


def test_load_too_big(tmpdir, override_settings):
    override_settings.set('MAX_SIZE', 5)
    m = tmpdir.join('main.py')
    m.write('123456')

    ft = FileTree.load(tmpdir.strpath)
    assert ft.children[0].name == 'main.py'
    assert ft.children[0].content is None
    assert ft.children[0].too_big
    assert ft.children[0].binary


def test_load_too_deep(tmpdir, override_settings):
    override_settings.set('MAX_DEPTH', 1)
    tmpdir.mkdir('first').mkdir('second').mkdir('third')
    ft = FileTree.load(tmpdir.strpath)
    assert ft.children[0].name == 'first'
    assert ft.children[0].children[0].name == FileTree.TOO_DEEP
    assert ft.children[0].children[0].children is None


def test_max_children(tmpdir, override_settings):
    override_settings.set('MAX_CHILDREN', 2)
    tmpdir.mkdir('a')
    tmpdir.mkdir('b')
    tmpdir.mkdir('c')

    ft = FileTree.load(tmpdir.strpath)
    assert len(ft.children) == 2


def test_load_etag(tmpdir, hasher):
    f = tmpdir.join('first.py')
    s = tmpdir.join('second.py')
    f.write('first')
    s.write('second')

    ft = FileTree.load(tmpdir.strpath, hasher)
    assert len(ft.children) == 2
    assert ft.children[0].name == 'first.py'
    assert ft.children[0].content == 'first'
    assert ft.children[0].changed
    assert ft.children[1].name == 'second.py'
    assert ft.children[1].content == 'second'
    assert ft.children[1].changed

    f.write('firstchanged')

    ft = FileTree.load(tmpdir.strpath, hasher)
    assert ft.children[0].name == 'first.py'
    assert ft.children[0].content == 'firstchanged'
    assert ft.children[0].changed
    assert ft.children[1].name == 'second.py'
    assert ft.children[1].content is None
    assert not ft.children[1].changed
