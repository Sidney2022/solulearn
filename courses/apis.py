class GetLoggedInUser(RetrieveAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Profile
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user
