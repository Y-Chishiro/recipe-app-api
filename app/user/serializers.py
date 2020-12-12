from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _  # 翻訳

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    # serializersを書くときは、まずはMetaを書く。
    class Meta:
        # まず、どのモデルかを指定する
        model = get_user_model()  # ここでモデルを指定！

        # 次にシリアライザーに含めたいフィールドを指定する。
        # ここに含めたフィールドがPOSTとかするときにJSONに含まれる。
        # APIでリード/ライト共にアクセシブルにしたいフィールド。
        fields = ('email', 'password', 'name')

        # 次にエクストラキーワード引数の指定。
        # パスワードは別に切り出す。
        # パスワードはWrite Onlyで、5文字以下はNGと伝える。
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        # validated_dataにはserializer内でValidationされた値が入る
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting hte password correctly and return it"""
        password = validated_data.pop('password', None)
        # もしユーザからのリクエストにパスワードが入っていたら取得して、Noneにする。

        user = super().update(instance, validated_data)
        # ModelSerializerクラスのupdateメソッドを呼ぶ。

        # パスワードがあるときだけ直接書き込む
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),  # contextは当該のPOSTリクエスト
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
