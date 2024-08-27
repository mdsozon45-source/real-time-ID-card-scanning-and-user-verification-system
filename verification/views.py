from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User, IDCard
from .serializers import UserSerializer, IDCardSerializer
from django.core.files.base import ContentFile
import numpy as np
import easyocr
from PIL import Image
import io
import re

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class IDCardViewSet(viewsets.ModelViewSet):
	queryset = IDCard.objects.all()
	serializer_class = IDCardSerializer

	def create(self, request, *args, **kwargs):
		image_file = request.FILES['scanned_image']
		user_id = request.data['user']
		id_number = request.data['id_number']

		# Extract text from image
		extracted_text = extract_text_from_image(image_file)
		print("Extracted Text:", extracted_text)  # Debug print

		# Parse the text
		parsed_data = parse_extracted_text(extracted_text)
		print("Parsed Data:", parsed_data)  # Debug print

		# Check ID number
		if id_number != parsed_data.get('id_number', ''):
		    return Response({"error": "ID number does not match the scanned document."},
		                    status=status.HTTP_400_BAD_REQUEST)

		# Perform face verification (placeholder logic here)
		user = User.objects.get(pk=user_id)
		user_image_path = user.photo.path
		if not verify_face(user_image_path, image_file):
		    return Response({"error": "Face does not match the user's profile."},
		                    status=status.HTTP_400_BAD_REQUEST)

		# Save the processed image and data
		id_card = IDCard.objects.create(
		    user_id=user_id,
		    id_number=parsed_data.get('id_number', ''),
		    scanned_image=ContentFile(image_file.read(), name='scan.jpg'),
		    verified=True
		)

		# Build the response with the image URL and other details
		response_data = {
		    "id_card": IDCardSerializer(id_card).data,
		    "scanned_image_url": id_card.scanned_image.url,
		    "extracted_data": parsed_data
		}

		return Response(response_data, status=status.HTTP_201_CREATED)

def extract_text_from_image(image_file):
    """Extract text from an image file using easyocr."""
    reader = easyocr.Reader(['en'])
    
    # Read image file
    img = Image.open(image_file)
    img = np.array(img)

    # Perform text detection
    results = reader.readtext(img)

    # Combine all detected texts into a single string
    extracted_text = ' '.join([text[1] for text in results])
    
    return extracted_text



def parse_extracted_text(text):
    """Parse the extracted text to find name, ID number, and birth date."""
    data = {}
    
    # Clean up text
    text = text.upper()
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    
    # Extract the name (Assuming name is between "NAME:" and next field)
    name_match = re.search(r'NAME:\s*([A-Z\s]+)', text)
    if name_match:
        data['name'] = name_match.group(1).strip()
    
    # Extract the ID number
    id_number_match = re.search(r'ID NO\s*([\d]+)', text)
    if id_number_match:
        data['id_number'] = id_number_match.group(1).strip()
    
    # Extract the birth date
    birth_date_match = re.search(r'DATE OF BIRTH\s*([\d-]+)', text)
    if birth_date_match:
        data['birth_date'] = birth_date_match.group(1).strip()
    
    return data

def verify_face(user_photo_path, id_photo_file):
    """Verify if the face in the ID photo matches the user's profile photo."""
    # Placeholder function
    return True
