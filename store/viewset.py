from rest_framework import mixins, viewsets


class CreateRetrieveViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):

    """
            A viewset that provides `retrieve` and `create` and `delete` actions.
    """
    pass


class CreateRetrieveUpdateViewSet(mixins.CreateModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  viewsets.GenericViewSet):
    """
            A viewset that provides `retrieve` and `create` and `update` actions.
    """
    pass
