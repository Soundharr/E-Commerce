# from rest_framework import serializers
# from django.db import transaction
# from .models import Order, OrderItem
# from products.models import Product

# class OrderItemSerializer(serializers.ModelSerializer):
#     product_title = serializers.CharField(source='product.title', read_only=True)

#     class Meta:
#         model = OrderItem
#         fields = ['id', 'product', 'product_title', 'quantity']
#         extra_kwargs = {
#             'product': {'required': True},
#             'quantity': {'required': True, 'min_value': 1}
#         }

# class OrderSerializer(serializers.ModelSerializer):
#     user_email = serializers.EmailField(source='user.email', read_only=True)
#     items = OrderItemSerializer(many=True)  # Updated field name to match related_name in the model

#     class Meta:
#         model = Order
#         fields = [
#             'id', 'first_name', 'last_name', 'user_email', 'mobile',
#             'door_no', 'area', 'city', 'state', 'pincode', 'date',
#             'total_amount', 'items',  # Updated field to 'items'
#         ]
#         read_only_fields = ['total_amount', 'user_email', 'date']

#     def create(self, validated_data):
#         validated_data.pop('user', None)  # Remove user from validated data
#         order_items_data = validated_data.pop('items')  # Adjusted to 'items' based on model's related_name

#         # Get the current user from the request context
#         user = self.context['request'].user

#         # Create the order object and associate it with the user
#         order = Order.objects.create(user=user, **validated_data)

#         total = 0
#         with transaction.atomic():  # Ensure all changes happen together
#             # Loop through the order items to calculate total and create the items
#             for item_data in order_items_data:
#                 product = item_data['product']
#                 quantity = item_data.get('quantity', 1)

#                 # Check if product is active and in stock
#                 if not product.is_active:
#                     raise serializers.ValidationError(f"Product {product.title} is not active.")
#                 if quantity > product.stock:
#                     raise serializers.ValidationError(f"Not enough stock for {product.title}.")

#                 # Create the order item and associate it with the order
#                 order_item = OrderItem.objects.create(order=order, **item_data)

#                 # Calculate total amount for the order
#                 total += order_item.get_total_price()  # Use get_total_price() from OrderItem

#             # Update the order's total amount and save it
#             order.total_amount = total
#             order.save()


#         return order


# serializers.py
from rest_framework import serializers
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from .models import Order, OrderItem
from products.models import Product  # Assuming 'Product' is in a separate 'products' app


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)
    product_stock = serializers.IntegerField(source='product.stock', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'product_price', 'product_stock', 'quantity']
        extra_kwargs = {
            'product': {'required': True},
            'quantity': {'required': True, 'min_value': 1}
        }


class OrderSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    items = OrderItemSerializer(many=True)  # Updated field name to match related_name in the model

    class Meta:
        model = Order
        fields = [
            'id', 'first_name', 'last_name', 'user_email', 'mobile',
            'door_no', 'area','street','city', 'state', 'pincode', 'date',
            'total_amount', 'items',  # Updated field to 'items'
        ]
        read_only_fields = ['total_amount', 'user_email', 'date']

    def create(self, validated_data):
        # Remove user from validated data and extract order items
        validated_data.pop('user', None)
        order_items_data = validated_data.pop('items')

        # Get the current user from the request context
        user = self.context['request'].user

        # Create the order object and associate it with the user
        order = Order.objects.create(user=user, **validated_data)

        total = 0
        with transaction.atomic():  # Ensure all changes happen together
            # Loop through the order items to calculate total and create the items
            for item_data in order_items_data:
                product = item_data['product']
                quantity = item_data.get('quantity', 1)

                # Check if product is active and in stock
                if not product.is_active:
                    raise serializers.ValidationError(f"Product {product.title} is not active.")
                if quantity > product.stock:
                    raise serializers.ValidationError(f"Not enough stock for {product.title}.")

                # Create the order item and associate it with the order
                order_item = OrderItem.objects.create(order=order, **item_data)

                # Calculate total amount for the order (Assuming get_total_price() exists)
                total += order_item.get_total_price()  # Use get_total_price() from OrderItem

            # Update the order's total amount and save it
            order.total_amount = total
            order.save()

        # Send email notifications (Optional)
        self.send_order_confirmation_email(user.email, order)
        self.send_new_order_notification_email(order)

        return order

    def send_order_confirmation_email(self, customer_email, order):
        """Send email confirmation to the customer."""
        subject = "Order Confirmation"
        message = f"Dear customer, your order #{order.id} has been successfully placed.\n\nTotal Amount: Rs.{order.total_amount}\n\nThank you for shopping with us."
        recipient_list = [customer_email]

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email to customer: {str(e)}")

    def send_new_order_notification_email(self, order):
        """Send email notification to the shop owner."""
        shop_owner_email = 'soundharraj458@gmail.com'  # Change this to your actual email address
        subject = f"New Order Received: #{order.id}"
        message = f"A new order has been placed.\n\nOrder ID: #{order.id}\nCustomer: {order.first_name} {order.last_name}\nTotal Amount: ${order.total_amount}\nShipping Address: {order.door_no}, {order.area}, {order.city}, {order.state}, {order.pincode}"
        recipient_list = [shop_owner_email]

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email to shop owner: {str(e)}")



# from rest_framework import serializers
# from django.db import transaction
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import Order, OrderItem
# from products.models import Product  # Assuming 'Product' is in a separate 'products' app


# class OrderItemSerializer(serializers.ModelSerializer):
#     product_title = serializers.CharField(source='product.title', read_only=True)
#     product_price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)
#     product_stock = serializers.IntegerField(source='product.stock', read_only=True)

#     class Meta:
#         model = OrderItem
#         fields = ['id', 'product', 'product_title', 'product_price', 'product_stock', 'quantity']
#         extra_kwargs = {
#             'product': {'required': True},
#             'quantity': {'required': True, 'min_value': 1}
#         }


# class OrderSerializer(serializers.ModelSerializer):
#     user_email = serializers.EmailField(source='user.email', read_only=True)
#     items = OrderItemSerializer(many=True)

#     class Meta:
#         model = Order
#         fields = [
#             'id', 'first_name', 'last_name', 'user_email', 'mobile',
#             'door_no', 'area', 'street', 'city', 'state', 'pincode', 'date',
#             'total_amount', 'items',
#         ]
#         read_only_fields = ['total_amount', 'user_email', 'date']

#     def create(self, validated_data):
#         order_items_data = validated_data.pop('items')
#         user = self.context['request'].user

#         with transaction.atomic():
#             order = Order.objects.create(user=user, **validated_data)
#             total = 0

#             for item_data in order_items_data:
#                 product = item_data['product']
#                 quantity = item_data.get('quantity', 1)

#                 if not product.is_active:
#                     raise serializers.ValidationError(f"Product {product.title} is not active.")
#                 if quantity > product.stock:
#                     raise serializers.ValidationError(f"Not enough stock for {product.title}.")

#                 order_item = OrderItem.objects.create(order=order, **item_data)
#                 total += order_item.get_total_price()

#                 # Reduce product stock
#                 product.stock -= quantity
#                 product.save()

#             order.total_amount = total
#             order.save()

#         # Send confirmation emails
#         self.send_order_confirmation_email(user.email, order)
#         self.send_new_order_notification_email(order)

#         return order

#     def send_order_confirmation_email(self, customer_email, order):
#         """Send detailed email to customer."""
#         subject = f"Order Confirmation - Order #{order.id}"
#         message = f"""
# Dear {order.first_name} {order.last_name},

# Your order #{order.id} has been successfully placed!

# 📦 Order Summary:
# ---------------------------
# Total Amount: ₹{order.total_amount}
# Ordered On: {order.date.strftime('%d-%m-%Y %I:%M %p')}

# 📍 Shipping Address:
# ---------------------------
# {order.door_no}, {order.area}, {order.street or ''}
# {order.city}, {order.state} - {order.pincode}

# 📞 Mobile: {order.mobile}
# 📧 Email: {customer_email}

# 🛒 Items:
# ---------------------------
# """

#         for item in order.items.all():
#             message += f"- {item.product_title} ({item.quantity}00g)\n"

#         message += "\nThank you for shopping with us!\n\nBest regards,\nCashew E-Commerce Team"

#         try:
#             send_mail(
#                 subject=subject,
#                 message=message,
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[customer_email],
#                 fail_silently=False,
#             )
#         except Exception as e:
#             print(f"Error sending confirmation email to customer: {e}")

#     def send_new_order_notification_email(self, order):
#         """Notify shop owner of new order."""
#         shop_owner_email = 'soundharraj458@gmail.com'  # Update as needed
#         subject = f"New Order Received - #{order.id}"
#         message = f"""
# A new order has been placed on your store!

# 🧾 Order ID: #{order.id}
# 👤 Customer: {order.first_name} {order.last_name}
# 📦 Total Amount: ₹{order.total_amount}

# 📍 Shipping Address:
# {order.door_no}, {order.area}, {order.street or ''}
# {order.city}, {order.state} - {order.pincode}

# 🛒 Items:
# """

#         for item in order.items.all():
#             message += f"- {item.product_title} ({item.quantity}00g)\n"

#         message += "\nCheck your admin panel for full details."

#         try:
#             send_mail(
#                 subject=subject,
#                 message=message,
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[shop_owner_email],
#                 fail_silently=False,
#             )
#         except Exception as e:
#             print(f"Error sending notification to shop owner: {e}")


from rest_framework import serializers
from .models import EnquiryForm

class EnquiryFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnquiryForm
        fields = '__all__'
