# Hello Habit

Приложение по формированию полезных привычек

## Gitflow

[master](https://gitlab.com/HelloHabit/hellohabit.telegram-bot/tree/master) - ветка содержит последнюю, стабильную версию для сборки и публикации приложения. Запрещены прямые пуши коммитов.

[develop](https://gitlab.com/HelloHabit/hellohabit.telegram-bot/tree/develop) - ветка содержит последнюю, стабильную версию для разработки и тестирования. Запрещены прямые пуши коммитов.

Разработка по каждой задаче осуществляется в своей ветке, унаследованной от последней версии [develop](https://gitlab.com/HelloHabit/hellohabit.telegram-bot/tree/develop), с обязательным указанием префикса (feature/bugfix/refactoring), кода доски, номера задачи и ключевого описания задачи:

```
refactoring/HH-100-optimization-navigator
```

После выполения задачи создается PR в ветку [develop](https://gitlab.com/HelloHabit/hellohabit.telegram-bot/tree/develop) с обязательным указанием префикса (feature/bugfix/refactoring), кода доски, номера задачи и описания выполенных работ. Если выполенные работы требуют пояснений, то они указываются в описании PR:

```
[refactoring/HH-100] Оптимизация рендеринга навигационного стэка
```

После прохождения код-ревью и тестирования, ветка вливается в develop и тестируется еще раз.

PR в [master](https://gitlab.com/HelloHabit/hellohabit.telegram-bot/tree/master) ветку принимаются только из [develop](https://gitlab.com/HelloHabit/hellohabit.telegram-bot/tree/develop) ветки.
