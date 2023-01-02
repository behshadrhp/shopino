from rest_framework import mixins, viewsets


class CreateRetrieveViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):

    """
            A viewset that provides `retrieve` and `create` actions.
        """
    pass
