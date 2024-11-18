class Person:
    def __init__(self, name, age):
        self.name = name  # 인스턴스 속성
        self.age = age

    def Explain(self):
        return f"이름 : { self.name }, 나이 : { self.age }"

Person1 = Person("지민섭", 14)
print(Person1.Explain())