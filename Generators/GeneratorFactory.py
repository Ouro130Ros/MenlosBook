from BasicGenerator import BasicGenerator

class GeneratorFactory:
    def get_generator(self, generator_name, level_config):
        if generator_name == "Basic":
            return BasicGenerator(level_config)
