from rest_framework import mixins, viewsets


class CreateRetrieveViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):

    """
            A viewset that provides `retrieve` and `create` actions.
        """
    pass
