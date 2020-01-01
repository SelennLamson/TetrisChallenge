from src.model import Model


def test_init_score():
    assert Model().score == 0


def test_current_tetro_not_null():
    assert Model.TETRO_I <= Model().current_tetro <= Model.TETRO_Z


def test_init_time_counter():
    assert Model().time_counter == 0


def test_init_rotation():
    assert Model().current_tetro_rotation == 0


def test_rotate():
    m = Model()
    m.rotate()
    assert m.current_tetro_rotation == 1
    m.rotate()
    assert m.current_tetro_rotation == 2
    m.rotate()
    assert m.current_tetro_rotation == 3
    m.rotate()
    assert m.current_tetro_rotation == 0


def test_init_position():
    m = Model()
    assert m.current_tetro_position == [23, 4]


def test_position_after_left_without_collision():
    m = Model()
    m.left()
    assert m.current_tetro_position == [23, 3]


def test_position_after_right_without_collision():
    m = Model()
    m.right()
    assert m.current_tetro_position == [23, 5]


def test_position_after_tick_without_collision():
    m = Model()
    m.tick()
    assert m.current_tetro_position == [22, 4]


def test_time_increased_after_tick():
    m = Model()
    assert m.time_counter == 0
    m.tick()
    assert m.time_counter == 1


def test_hold_with_empty():
    m = Model()
    p1 = m.current_tetro
    p2 = m.next_tetro
    assert m.held_tetro is None
    m.hold()
    assert m.held_tetro == p1
    assert m.current_tetro == p2


def test_hold_with_held_tetro():
    m = Model()
    m.hold()

    p1 = m.current_tetro
    assert m.held_tetro is not None
    p2 = m.held_tetro

    m.hold()

    assert m.current_tetro == p2
    assert m.held_tetro == p1
