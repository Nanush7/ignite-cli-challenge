# ignite-cli-challenge
Prometeo Command Line Interface.

## Requirements
 - Python >= 3.8 (tested on 3.8.12).

## Install

1. Clone repo.
2. Create virtual environment (optional).
3. Run `pip3 install -r requirements.txt`

## How to use
Simply run `python3 main.py`

You may see available options with `python3 main.py -h`.

## Creating plugins

This repo comes with 3 basic plugins, but you may create your own using the BasePlugin class.

First, you must create a file inside the plugins folder named like `*_plugin.py`.

Inside that file, add the following:

```python
import src.plugins as plugins

class YourPluginName(plugins.BasePlugin):
    plugin_name = 'PluginName'
    plugin_description = 'Plugin Description.'

    def __init__(self, client, output):
        # Add anything you want here.
        super().__init__(client, output)

    def run(self) -> None:
        # This method is required.
        # This will be the main function of your plugin.
        # ...

    def close(self) -> None:
        # This method is optional.
        # It will be executed upon closing the CLI.
        # For example, it's used in the sessions plugin
        # to logout before closing.
        # ...
```

The `BasePlugin` class provides the following attributes that you may use in your plugin class:

1. `self.client`: this is a PrometeoClient instance which provides API methods. Like login, logout, providers, etc.

self.client provides a `self.status` attribute indicating the session status and other attributes you may want to use (look at client.py for more info).

You will probably want to make modifications to the client instance, as it will be accessible to all plugins. Have a look at `sessions_plugin.py` for more information.

2. `self.out`: this provides output methods available in `output.py`. Have a look at it for more information. **RECOMMENDATION**: use this instead of `print()`.
3. `self.utils`: this one provides input methods available in `utils.py`. Have a look at it for more information. **RECOMMENDATION**: use this instead of `input()`.

Inside utils, you have a `get_option` method:
```python
    def get_option(self, type: str = 'int', required: bool = True, input_prefix: str = DEFAULT_INPUT_PREFIX, extra_validation: Callable = None) -> Any: ...
```
Params (all of them are optional):
 - type: the type of input you want. Must be one of AVAILABLE_DATATYPES (in config.py).
 - required: if set to True, it will ask the user for input until a valid input is given. If False, a blank input returns `None`.
 - input_prefix: This is displayed when asking for user input, like this: `input(input_prefix)`.
 - extra_validation: this param must be a callable object. It will be executed as additional input validation. Below you have more instructions on this.

 Creating a validation method:

 ```python
class YourPluginName(plugins.BasePlugin):
 
    # ...

    def run(self):
        # ...
        option = self.utils.get_options(extra_validation=self.example_validation)
        # ...

    def example_validation(self, data) -> None:  # data param is required.
        # Magic.
        # ...
        # Magic goes wrong:

        raise ValidationError
        # This exception class is inherited from BasePlugin.
        # There is no need to import it.
        # You should raise this exception somewhere.
 ```

**RECOMMENDATION**: read output.py and utils.py to see more methods available.
