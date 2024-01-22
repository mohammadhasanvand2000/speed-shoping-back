from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from .models import User
from .serializers import SetNewPasswordSerializer,ResetPasswordEmailRequestSerializer
from django.contrib.sessions.models import Session

from .models import User
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .Util import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .serializers import ResetPasswordEmailRequestSerializer
from .models import User
from django.utils.translation import gettext as _
from .Util import Util
from django.shortcuts import redirect



@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer








class RequestPasswordResetEmail(GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(str(user.id).encode())
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            relative_link = reverse(
                'password_reset_confrim', kwargs={'uidb64': uidb64, 'token': token}
            )
            abs_url = 'http://' + current_site + relative_link
            email_body = f"برای بازیابی رمز عبور خود، لطفاً روی لینک زیر کلیک کنید:\n{abs_url}"
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': _('بازیابی رمز عبور')}
            Util.send_email(data)
            return Response({'message': _('ایمیل بازیابی رمز عبور با موفقیت ارسال شد.')}, status=status.HTTP_200_OK)
        else:
            return Response({'message': _('کاربری با این ایمیل وجود ندارد.')}, status=status.HTTP_400_BAD_REQUEST)
        
class PasswordTokenCheckAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'})

            # Redirect to the SetNewPasswordAPI URL
            redirect_url = reverse('reset_password_complate', args=[uidb64, token])
            return redirect(redirect_url)

        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': 'توکن صحیح نیست، دوباره امتحان کنید'})



from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, serializers, status
from rest_framework.response import Response

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.translation import gettext as _

from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.encoding import force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import redirect
from django.urls import reverse

from django.shortcuts import redirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import SetNewPasswordSerializer
from .models import User

class SetNewPasswordAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64', "")
        token = kwargs.get('token', "")

        if uidb64 and token:
            try:
                id = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(id=id)

                if not PasswordResetTokenGenerator().check_token(user, token):
                    raise serializers.ValidationError(_("No valid link"))

            except DjangoUnicodeDecodeError as e:
                raise serializers.ValidationError(_("Invalid link"))

        # اگر همه‌چیز درست باشد، انجام تغییرات و بازگشت به صفحه فرانت‌اند
        return redirect('http://localhost:3000/Setnewpassword/{}/{}'.format(uidb64, token))

    def patch(self, request, *args, **kwargs):
        uidb64 = request.data.get('uidb64', "")
        token = request.data.get('token', "")

        if not uidb64 or not token:
            raise serializers.ValidationError(_("Invalid link"))

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(_("No valid link"))

            password = request.data.get('password')
            user.set_password(password)
            user.save()

            return Response({'success': True, 'message': 'Password successfully changed'}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as e:
            raise serializers.ValidationError(_("Invalid link"))
