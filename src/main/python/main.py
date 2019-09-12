from fbs_runtime.application_context.PyQt5 import ApplicationContext
import img2url
import sys


if __name__ == '__main__':
    app_context = ApplicationContext()
    window = img2url.Img2url(app_context.app)
    window.show()
    sys.exit(app_context.app.exec_())
