class Tag:
    def __init__(self, name, replacement_function):
        self.name = name
        self.replacement_function = replacement_function

    def replace(self, content, context):
        if self.name in content:
            replacement_value = self.replacement_function(context)
            content = content.replace(self.name, replacement_value)
        return content
