from rest_framework import serializers

from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=4, required=True)

    class Meta: 
        model = User
        fields = ('email', 'password', 'password_confirm', 'first_name', 'last_name', 'phone',)
    
    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password_confirm')
        if p1 != p2:
            raise serializers.ValidationError("Passwords not match")
        return attrs
    
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with email already exists")
        return email

    def validate_phone(self, phone):
        if len(phone) > 13:
            raise serializers.ValidationError("The number should be max 13 digits")
        return phone
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class CreateNewPasswordSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=150, required=True)
    activation_code = serializers.CharField(max_length=8, min_length=8, required=True)
    password = serializers.CharField(min_length=8, required=True)
    password_confirm = serializers.CharField(min_length=8, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'activation_code')

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователя с таким email не найден')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        email = data.get('email')
        password = data.get('password')
        try:
            user = User.objects.get(email=email)
            if not user:
                raise serializers.ValidationError('Пользователь не найден')
        except User.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден')

        user.set_password(password)
        user.save()
        return user