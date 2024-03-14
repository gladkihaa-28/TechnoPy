class Defence:
    @staticmethod
    def parsing_defence(request):
        if "request" in request.headers.get('User-Agent'):
            return False
        return True
