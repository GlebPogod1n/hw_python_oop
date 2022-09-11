from dataclasses import asdict, dataclass, field


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = (
        'Тип тренировки: {training_type};'
        ' Длительность: {duration:.3f} ч.;'
        ' Дистанция: {distance:.3f} км;'
        ' Ср. скорость: {speed:.3f} км/ч;'
        ' Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    M_IN_KM: float = field(default=1000, init=False)
    LEN_STEP: float = field(default=0.65, init=False)
    M_IN_H: float = field(default=60, init=False)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(self.__class__.__name__)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIE_RATIO_RUN_1: float = 18
    CALORIE_RATIO_RUN_2: float = 20

    def get_spent_calories(self) -> float:
        return ((self.CALORIE_RATIO_RUN_1 * self.get_mean_speed()
                - self.CALORIE_RATIO_RUN_2) * self.weight / self.M_IN_KM
                * self.duration * self.M_IN_H)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    CALORIE_RATIO_WALK_1: float = 0.035
    CALORIE_RATIO_WALK_2: float = 0.029

    def get_spent_calories(self) -> float:
        return ((self.CALORIE_RATIO_WALK_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.CALORIE_RATIO_WALK_2 * self.weight)
                * self.duration * self.M_IN_H)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: float
    LEN_STEP: float = field(default=1.38, init=False)
    CALORIE_RATIO_SWIM_1: float = 1.1
    CALORIE_RATIO_SWIM_2: float = 2

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIE_RATIO_SWIM_1)
                * self.CALORIE_RATIO_SWIM_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types = {'RUN': Running,
                     'WLK': SportsWalking,
                     'SWM': Swimming}
# Тут буду рад информации как красиво проконтролировать аргументы#
    if workout_type in workout_types:
        return workout_types[workout_type](*data)
    else:
        return NameError('Неизвестный тип тренировки!')


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]), ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
