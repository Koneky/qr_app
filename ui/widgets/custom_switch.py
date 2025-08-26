from kivy.properties import BooleanProperty, ListProperty
from kivymd.uix.button import MDIconButton
from kivy.metrics import dp


class CustomSwitch(MDIconButton):
    """
    Лёгкий кастомный переключатель - визуально похож на toggle switch,
    но полностью контролируется из кода (цвета, иконки, размер).
    Использование: в KV импортировать/зарегистрировать класс и поставить
    `CustomSwitch` вместо MDSwitch. Свойство `active` можно биндиговать.
    """
    active = BooleanProperty(False)
    active_color = ListProperty([0.298, 0.686, 0.314, 1])
    inactive_color = ListProperty([0.6, 0.6, 0.6, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # фиксированный размер, чтобы не "выскакивал" из строки
        self.size_hint = (None, None)
        self.size = (dp(52), dp(32))

        # начальные визуальные настройки
        self.theme_text_color = "Custom"
        self.text_color = [1, 1, 1, 1]

        # убедимся, что визуал соответсвует начальному состоянию
        self._apply_visual()

        # биндим обновление внешнего вида при смене active
        self.bind(active=self.on_active)

    def on_release(self, *args):
        """
        Кликаем - переключаем состояние и применяем визуал.
        При этом корректно вызываем суперкласс (примет или не примет args)
        """
        # переключаем логическое состояние
        self.active = not self.active
        # визуально применяем (on_active также вызывается)
        self._apply_visual()
        # попытка вызвать super с args, если API допускает
        try:
            return super().on_release(*args)
        except TypeError:
            return super().on_release()

    def on_active(self, instance, value):
        """
        Обработчик на изменение свойства active (вызван автоматически).
        """
        self._apply_visual()

    def _apply_visual(self):
        """
        Единая функция, которая применяет иконку и цвет в зависимости от active. 
        """
        if self.active:
            self.icon = "toggle-switch"
            self.md_bg_color = self.active_color
        else:
            self.icon = "toggle-switch-off-outline"
            self.md_bg_color = self.inactive_color