from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='barrywhite',
        password='minha_senha_123',
        email='barrywhite@barrylabs.com',
    )

    session.add(user)
    session.commit()
    # session.refresh(user)

    result = session.scalar(
        select(User).where(User.email == 'barrywhite@barrylabs.com')
    )

    assert result.id == 1
    assert result.username == 'barrywhite'
