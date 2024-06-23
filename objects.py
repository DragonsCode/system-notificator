from dataclasses import dataclass

@dataclass
class Usage:
    """
    Класс для хранения информации о потреблении памяти диска или ОЗУ
    """
    component: str
    available: float
    used: float
    total: float
    available_percent: float
    used_percent: float

    def __str__(self):
        return (
        f"{self.component}:\n"
        f"Доступно: {self.available} MB\n"
        f"Использовано: {self.used} MB\n"
        f"Всего: {self.total} MB\n\n"
        f"Доступно %: {self.available_percent}%\n"
        f"Использовано %: {self.used_percent}%\n"
        )