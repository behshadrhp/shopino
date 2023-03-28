from django.shortcuts import render
from logging import getLogger

# Create your views here.

logger = getLogger(__name__)

def home(request):
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
    return render(request, 'src/main.html')
