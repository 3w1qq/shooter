# Шутер
Это [игра-шутер](https://ru.wikipedia.org/wiki/Шутер 'Что такое "Шутер"?'), написанная на языке Python.  
Используемые библиотекии и модули: 
* PyGame
* random
* time

Цель игры заключается в том, чтобы сбить 10 НЛО и не задеть врагов, либо астероиды. Всего 3 жизни -- от одного касания по врагу снимается одна жизнь.

![Скриншот](https://raw.githubusercontent.com/3w1qq/shooter/refs/heads/main/screen%20shooter%20.png?token=GHSAT0AAAAAADJVIYRH43KCXYCVR3C7Z2NU2FQS6DQ)

### Пример кода:

```python
class Player(GameSprite):
    def move(self):
        keys_pressed = p.key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        elif keys_pressed[K_d] and self.rect.x < win_width - rocket_width:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', 5, self.rect.centerx - bullet_width / 2, self.rect.top, bullet_width, 20)
        bullets.add(bullet)
        fire.play()
```

###   СМИ о нас:

***Журнал "Все об играх":***

> Лучшая игра 2025 года!

***Канал "Оптимизация игр"***

> Игру тянет любой, даже слабый компьютер 
