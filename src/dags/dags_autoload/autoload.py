import importlib
import sys
import inspect

def require_module(module: str, context: str = ""):
    '''
    Importa um módulo.

    Parameters:
        module (str): Módulo a ser importado (Required).

        context (str): Caminho para a raiz da aplicação (Default "").

    Returns:
        <module: 'package.module'>
    '''
    try:
        __APP_NAME__ = context if context != "" else context
        return importlib.import_module(f'{__APP_NAME__}{module}')
    except Exception as e:
        print(str(e))


def require_class(module: str, class_name: str = "", context: str = ""):
    '''
    Importa uma ou mais classes de um módulo.

    Parameters:
        module (str): Módulo a ser importado (Required).

        class_name (str): Nome da classe que deve ser retornada (Default "")
            Retorna a primeira classe do módulo caso o parâmetro class_name não seja passado.

        context (str): Caminho para a raiz da aplicação (Default "").

    Returns:
        <class: 'package.module.Class'>
    '''
    try:
        mod = require_module(module, context)
        classes = {}
        for _, obj in inspect.getmembers(sys.modules[mod.__name__], inspect.isclass):
            if inspect.isclass(obj) and obj.__name__ != "BaseOperator":
                classes[obj.__name__] = obj

        if not classes:
            raise Exception(f"Nenhuma classe encontrada no módulo {mod.__name__}")

        return list(classes.values())[0] if class_name == "" else classes.get(class_name)
    except Exception as e:
        print(str(e))
