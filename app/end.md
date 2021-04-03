openapi: 3.0.2
info:
  title: ''
  version: ''
paths:
  /api/user/:
    get:
      operationId: listUsers
      description: ''
      parameters: []
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
          description: ''
      tags:
      - api
  /api/user/{id}/:
    get:
      operationId: retrieveUser
      description: ''
      parameters:
      - name: id
        in: path
        required: true
        description: "A unique value identifying this \u30E6\u30FC\u30B6\u30FC."
        schema:
          type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
          description: ''
      tags:
      - api
  /api/profile/:
    get:
      operationId: listProfiles
      description: for your own profile
      parameters: []
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Profile'
          description: ''
      tags:
      - api
  /api/profile/{id}/:
    get:
      operationId: retrieveProfile
      description: for your own profile
      parameters:
      - name: id
        in: path
        required: true
        description: A unique value identifying this profile.
        schema:
          type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Profile'
          description: ''
      tags:
      - api
    put:
      operationId: updateProfile
      description: for your own profile
      parameters:
      - name: id
        in: path
        required: true
        description: A unique value identifying this profile.
        schema:
          type: string
      requestBody:
        content:
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Profile'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Profile'
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Profile'
          description: ''
      tags:
      - api
    patch:
      operationId: partialUpdateProfile
      description: for your own profile
      parameters:
      - name: id
        in: path
        required: true
        description: A unique value identifying this profile.
        schema:
          type: string
      requestBody:
        content:
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Profile'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Profile'
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Profile'
          description: ''
      tags:
      - api
  /api/allprofile/:
    get:
      operationId: listProfiles
      description: ''
      parameters: []
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Profile'
          description: ''
      tags:
      - api
  /api/allprofile/{id}/:
    get:
      operationId: retrieveProfile
      description: ''
      parameters:
      - name: id
        in: path
        required: true
        description: A unique value identifying this profile.
        schema:
          type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Profile'
          description: ''
      tags:
      - api
  /api/category/:
    get:
      operationId: listCategorys
      description: "for list category view \n\ndisplay category related product !"
      parameters: []
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Category'
          description: ''
      tags:
      - api
  /api/brand/:
    get:
      operationId: listBrands
      description: "for list brand view \n\ndisplay brand related product !"
      parameters: []
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Brand'
          description: ''
      tags:
      - api
  /api/tag/:
    get:
      operationId: listTags
      description: "for list tag view \n\ndisplay tag related product !"
      parameters: []
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Tag'
          description: ''
      tags:
      - api
  /api/product-category/:
    get:
      operationId: listProducts
      description: 'filter by brand/<category_name_slug>

        display Respective Category Products !'
      parameters: []
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Product'
          description: ''
      tags:
      - api
  /api/product-brand/:
    get:
      operationId: listProducts
      description: 'filter by brand/<brand_name_slug>

        display Respective Brand Pens !'
      parameters: []
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Product'
          description: ''
      tags:
      - api
  /api/product-tag/:
    get:
      operationId: listProducts
      description: 'filter by tag

        display Respective Tag Products !'
      parameters: []
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Product'
          description: ''
      tags:
      - api
  /api/search/:
    get:
      operationId: listProducts
      description: search like below
      parameters:
      - name: name
        required: false
        in: query
        description: name
        schema:
          type: string
      - name: tag
        required: false
        in: query
        description: tag
        schema:
          type: string
      - name: brand
        required: false
        in: query
        description: brand
        schema:
          type: string
      - name: category
        required: false
        in: query
        description: category
        schema:
          type: string
      - name: lte
        required: false
        in: query
        description: lte
        schema:
          type: string
      - name: gte
        required: false
        in: query
        description: gte
        schema:
          type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Product'
          description: ''
      tags:
      - api
  /api/fav/:
    get:
      operationId: listFavProducts
      description: 'get specific fav info

        EX'
      parameters:
      - name: fav_user
        required: false
        in: query
        description: fav_user
        schema:
          type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/FavProduct'
          description: ''
      tags:
      - api
  /api/fav/{id}/:
    get:
      operationId: retrieveFavProduct
      description: 'get specific fav info

        EX'
      parameters:
      - name: id
        in: path
        required: true
        description: A unique integer value identifying this fav product.
        schema:
          type: string
      - name: fav_user
        required: false
        in: query
        description: fav_user
        schema:
          type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FavProduct'
          description: ''
      tags:
      - api
  /api/fav/{id}/check_fav/:
    get:
      operationId: checkFavFavProduct
      description: 'get specific fav info

        EX'
      parameters:
      - name: id
        in: path
        required: true
        description: A unique integer value identifying this fav product.
        schema:
          type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FavProduct'
          description: ''
      tags:
      - api
  /api/products/:
    get:
      operationId: listProducts
      description: ''
      parameters: []
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Product'
          description: ''
      tags:
      - api
  /api/products/{id}/:
    get:
      operationId: retrieveProduct
      description: ''
      parameters:
      - name: id
        in: path
        required: true
        description: A unique value identifying this product.
        schema:
          type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Product'
          description: ''
      tags:
      - api
  /api/review/:
    get:
      operationId: listReviews
      description: "can review specific pen \nonly authenticateed user"
      parameters: []
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ReviewSerialier'
          description: ''
      tags:
      - api
  /api/review/{id}/:
    get:
      operationId: retrieveReview
      description: "can review specific pen \nonly authenticateed user"
      parameters:
      - name: id
        in: path
        required: true
        description: A unique value identifying this review.
        schema:
          type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ReviewSerialier'
          description: ''
      tags:
      - api
  /api/my-review/:
    get:
      operationId: listReviews
      description: View that get data reviewed by request user:IsAuthenticated
      parameters: []
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ReviewSerialier'
          description: ''
      tags:
      - api
  /api/my-review/{id}/:
    get:
      operationId: retrieveReview
      description: View that get data reviewed by request user:IsAuthenticated
      parameters:
      - name: id
        in: path
        required: true
        description: A unique value identifying this review.
        schema:
          type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ReviewSerialier'
          description: ''
      tags:
      - api
    put:
      operationId: updateReview
      description: View that get data reviewed by request user:IsAuthenticated
      parameters:
      - name: id
        in: path
        required: true
        description: A unique value identifying this review.
        schema:
          type: string
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ReviewSerialier'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/ReviewSerialier'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/ReviewSerialier'
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ReviewSerialier'
          description: ''
      tags:
      - api
    patch:
      operationId: partialUpdateReview
      description: View that get data reviewed by request user:IsAuthenticated
      parameters:
      - name: id
        in: path
        required: true
        description: A unique value identifying this review.
        schema:
          type: string
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ReviewSerialier'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/ReviewSerialier'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/ReviewSerialier'
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ReviewSerialier'
          description: ''
      tags:
      - api
  /dj/logout/:
    get:
      operationId: listLogouts
      description: 'Calls Django logout method and delete the Token object

        assigned to the current User object.


        Accepts/Returns nothing.'
      parameters: []
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items: {}
          description: ''
      tags:
      - dj
    post:
      operationId: createLogout
      description: 'Calls Django logout method and delete the Token object

        assigned to the current User object.


        Accepts/Returns nothing.'
      parameters: []
      requestBody:
        content:
          application/json:
            schema: {}
          application/x-www-form-urlencoded:
            schema: {}
          multipart/form-data:
            schema: {}
      responses:
        '201':
          content:
            application/json:
              schema: {}
          description: ''
      tags:
      - dj
  /dj/user/:
    get:
      operationId: retrieveUserDetails
      description: 'Reads and updates UserModel fields

        Accepts GET, PUT, PATCH methods.


        Default accepted fields: username, first_name, last_name

        Default display fields: pk, username, email, first_name, last_name

        Read-only fields: pk, email


        Returns UserModel fields.'
      parameters: []
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserDetails'
          description: ''
      tags:
      - dj
    put:
      operationId: updateUserDetails
      description: 'Reads and updates UserModel fields

        Accepts GET, PUT, PATCH methods.


        Default accepted fields: username, first_name, last_name

        Default display fields: pk, username, email, first_name, last_name

        Read-only fields: pk, email


        Returns UserModel fields.'
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserDetails'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/UserDetails'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/UserDetails'
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserDetails'
          description: ''
      tags:
      - dj
    patch:
      operationId: partialUpdateUserDetails
      description: 'Reads and updates UserModel fields

        Accepts GET, PUT, PATCH methods.


        Default accepted fields: username, first_name, last_name

        Default display fields: pk, username, email, first_name, last_name

        Read-only fields: pk, email


        Returns UserModel fields.'
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserDetails'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/UserDetails'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/UserDetails'
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserDetails'
          description: ''
      tags:
      - dj
  /api/login/:
    post:
      operationId: createSocialLogin
      description: ''
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SocialLogin'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/SocialLogin'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/SocialLogin'
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SocialLogin'
          description: ''
      tags:
      - api
  /api/logout/:
    post:
      operationId: createLogout
      description: ''
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Logout'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Logout'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Logout'
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Logout'
          description: ''
      tags:
      - api
  /api/token/refresh/:
    post:
      operationId: createTokenRefresh
      description: 'Takes a refresh type JSON web token and returns an access type
        JSON web

        token if the refresh token is valid.'
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TokenRefresh'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/TokenRefresh'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/TokenRefresh'
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TokenRefresh'
          description: ''
      tags:
      - api
  /api/token/verify/:
    post:
      operationId: createTokenVerify
      description: 'Takes a token and indicates if it is valid.  This view provides
        no

        information about a token''s fitness for a particular use.'
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TokenVerify'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/TokenVerify'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/TokenVerify'
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TokenVerify'
          description: ''
      tags:
      - api
  /api/fav/{id}/fav/:
    post:
      operationId: favFavProduct
      description: 'FAV

        default false

        if not faved => fav

        product = models.Product.objects.get(id=pk)'
      parameters:
      - name: id
        in: path
        required: true
        description: A unique integer value identifying this fav product.
        schema:
          type: string
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/FavProduct'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/FavProduct'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/FavProduct'
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FavProduct'
          description: ''
      tags:
      - api
  /api/review/{id}/create_review/:
    post:
      operationId: createReviewReview
      description: "review specific pen \nex) http://localhost:8000/api/review/<int:product_id>/create_review/"
      parameters:
      - name: id
        in: path
        required: true
        description: A unique value identifying this review.
        schema:
          type: string
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ReviewSerialier'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/ReviewSerialier'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/ReviewSerialier'
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ReviewSerialier'
          description: ''
      tags:
      - api
  /dj/password/reset/:
    post:
      operationId: createPasswordReset
      description: 'Calls Django Auth PasswordResetForm save method.


        Accepts the following POST parameters: email

        Returns the success/fail message.'
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PasswordReset'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PasswordReset'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PasswordReset'
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PasswordReset'
          description: ''
      tags:
      - dj
  /dj/password/reset/confirm/:
    post:
      operationId: createPasswordResetConfirm
      description: "Password reset e-mail link is confirmed, therefore\nthis resets\
        \ the user's password.\n\nAccepts the following POST parameters: token, uid,\n\
        \    new_password1, new_password2\nReturns the success/fail message."
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PasswordResetConfirm'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PasswordResetConfirm'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PasswordResetConfirm'
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PasswordResetConfirm'
          description: ''
      tags:
      - dj
  /dj/login/:
    post:
      operationId: createLogin
      description: 'Check the credentials and return the REST Token

        if the credentials are valid and authenticated.

        Calls Django Auth login method to register User ID

        in Django session framework


        Accept the following POST parameters: username, password

        Return the REST Framework Token Object''s key.'
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Login'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/Login'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/Login'
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Login'
          description: ''
      tags:
      - dj
  /dj/password/change/:
    post:
      operationId: createPasswordChange
      description: 'Calls Django Auth SetPasswordForm save method.


        Accepts the following POST parameters: new_password1, new_password2

        Returns the success/fail message.'
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PasswordChange'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/PasswordChange'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/PasswordChange'
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PasswordChange'
          description: ''
      tags:
      - dj
  /dj/token/verify/:
    post:
      operationId: createTokenVerify
      description: 'Takes a token and indicates if it is valid.  This view provides
        no

        information about a token''s fitness for a particular use.'
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TokenVerify'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/TokenVerify'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/TokenVerify'
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TokenVerify'
          description: ''
      tags:
      - dj
  /dj/token/refresh/:
    post:
      operationId: createCookieTokenRefresh
      description: ''
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CookieTokenRefresh'
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/CookieTokenRefresh'
          multipart/form-data:
            schema:
              $ref: '#/components/schemas/CookieTokenRefresh'
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CookieTokenRefresh'
          description: ''
      tags:
      - dj
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          readOnly: true
        profile:
          type: string
        nickname:
          type: string
          readOnly: true
        twitter_account:
          type: string
          readOnly: true
        avatar:
          type: string
          readOnly: true
      required:
      - profile
    Profile:
      type: object
      properties:
        id:
          type: string
          readOnly: true
        nickname:
          type: string
          maxLength: 10
        review:
          type: string
          readOnly: true
        faved_product:
          type: string
          readOnly: true
        created_at:
          type: string
          format: date
          readOnly: true
        updated_at:
          type: string
          format: date
          readOnly: true
        avatar:
          type: string
          readOnly: true
    Category:
      type: object
      properties:
        name:
          type: string
          maxLength: 50
        slug:
          type: string
          maxLength: 50
        product_category:
          type: array
          items:
            type: string
      required:
      - name
      - slug
      - product_category
    Brand:
      type: object
      properties:
        id:
          type: integer
          readOnly: true
        name:
          type: string
          maxLength: 50
        slug:
          type: string
          maxLength: 50
        official_site_link:
          type: string
          maxLength: 255
      required:
      - name
      - slug
      - official_site_link
    Tag:
      type: object
      properties:
        name:
          type: string
          maxLength: 50
        slug:
          type: string
          maxLength: 50
        product_tag:
          type: array
          items:
            type: string
      required:
      - name
      - slug
      - product_tag
    Product:
      type: object
      properties:
        id:
          type: string
          readOnly: true
        name:
          type: string
          readOnly: true
        description:
          type: string
          readOnly: true
        price_yen:
          type: integer
          readOnly: true
        image:
          type: string
          format: binary
          readOnly: true
        image_src:
          type: string
          readOnly: true
        amazon_link_to_buy:
          type: string
          readOnly: true
        rakuten_link_to_buy:
          type: string
          readOnly: true
        mercari_link_to_buy:
          type: string
          readOnly: true
        number_of_review:
          type: string
          readOnly: true
        avarage_of_review_star:
          type: string
          readOnly: true
        review:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                readOnly: true
              title:
                type: string
                maxLength: 100
              stars_of_design:
                type: integer
                maximum: 5
                minimum: 1
              stars_of_durability:
                type: integer
                maximum: 5
                minimum: 1
              stars_of_usefulness:
                type: integer
                maximum: 5
                minimum: 1
              stars_of_function:
                type: integer
                maximum: 5
                minimum: 1
              stars_of_easy_to_get:
                type: integer
                maximum: 5
                minimum: 1
              avarage_star:
                type: string
                readOnly: true
              good_point_text:
                type: string
                nullable: true
              bad_point_text:
                type: string
                nullable: true
              reviewer:
                type: object
                properties:
                  id:
                    type: string
                    readOnly: true
                  profile:
                    type: string
                  nickname:
                    type: string
                    readOnly: true
                  twitter_account:
                    type: string
                    readOnly: true
                  avatar:
                    type: string
                    readOnly: true
                required:
                - profile
                readOnly: true
              created_at:
                type: string
                format: date-time
                readOnly: true
            required:
            - title
            - stars_of_design
            - stars_of_durability
            - stars_of_usefulness
            - stars_of_function
            - stars_of_easy_to_get
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true
        category:
          type: object
          properties:
            id:
              type: integer
              readOnly: true
            name:
              type: string
              maxLength: 50
          required:
          - name
          readOnly: true
        brand:
          type: object
          properties:
            id:
              type: integer
              readOnly: true
            name:
              type: string
              maxLength: 50
            slug:
              type: string
              maxLength: 50
            official_site_link:
              type: string
              maxLength: 255
          required:
          - name
          - slug
          - official_site_link
          readOnly: true
        tag:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
                maxLength: 50
              slug:
                type: string
                maxLength: 50
            required:
            - name
            - slug
          readOnly: true
      required:
      - review
    FavProduct:
      type: object
      properties:
        is_favorite:
          type: boolean
          readOnly: true
        fav_user:
          type: string
        product:
          type: string
        created_at:
          type: string
          format: date-time
          readOnly: true
      required:
      - fav_user
      - product
    ReviewSerialier:
      type: object
      properties:
        id:
          type: string
          readOnly: true
        title:
          type: string
          maxLength: 100
        stars_of_design:
          type: integer
          maximum: 5
          minimum: 1
        stars_of_durability:
          type: integer
          maximum: 5
          minimum: 1
        stars_of_usefulness:
          type: integer
          maximum: 5
          minimum: 1
        stars_of_function:
          type: integer
          maximum: 5
          minimum: 1
        stars_of_easy_to_get:
          type: integer
          maximum: 5
          minimum: 1
        avarage_star:
          type: string
          readOnly: true
        good_point_text:
          type: string
          nullable: true
        bad_point_text:
          type: string
          nullable: true
        reviewer:
          type: object
          properties:
            id:
              type: string
              readOnly: true
            profile:
              type: string
            nickname:
              type: string
              readOnly: true
            twitter_account:
              type: string
              readOnly: true
            avatar:
              type: string
              readOnly: true
          required:
          - profile
          readOnly: true
        created_at:
          type: string
          format: date-time
          readOnly: true
      required:
      - title
      - stars_of_design
      - stars_of_durability
      - stars_of_usefulness
      - stars_of_function
      - stars_of_easy_to_get
    UserDetails:
      type: object
      properties:
        pk:
          type: string
          readOnly: true
        username:
          type: string
          description: "\u3053\u306E\u9805\u76EE\u306F\u5FC5\u9808\u3067\u3059\u3002\
            \u534A\u89D2\u30A2\u30EB\u30D5\u30A1\u30D9\u30C3\u30C8\u3001\u534A\u89D2\
            \u6570\u5B57\u3001@/./+/-/_ \u3067150\u6587\u5B57\u4EE5\u4E0B\u306B\u3057\
            \u3066\u304F\u3060\u3055\u3044\u3002"
          pattern: ^[\w.@+-]+\z
          maxLength: 150
        email:
          type: string
          format: email
          readOnly: true
        first_name:
          type: string
          maxLength: 150
        last_name:
          type: string
          maxLength: 150
      required:
      - username
    SocialLogin:
      type: object
      properties:
        access_token:
          type: string
        code:
          type: string
        id_token:
          type: string
    Logout:
      type: object
      properties:
        refresh:
          type: string
      required:
      - refresh
    TokenRefresh:
      type: object
      properties:
        refresh:
          type: string
      required:
      - refresh
    TokenVerify:
      type: object
      properties:
        token:
          type: string
      required:
      - token
    PasswordReset:
      type: object
      properties:
        email:
          type: string
          format: email
      required:
      - email
    PasswordResetConfirm:
      type: object
      properties:
        new_password1:
          type: string
          maxLength: 128
        new_password2:
          type: string
          maxLength: 128
        uid:
          type: string
        token:
          type: string
      required:
      - new_password1
      - new_password2
      - uid
      - token
    Login:
      type: object
      properties:
        username:
          type: string
        email:
          type: string
          format: email
        password:
          type: string
      required:
      - password
    PasswordChange:
      type: object
      properties:
        new_password1:
          type: string
          maxLength: 128
        new_password2:
          type: string
          maxLength: 128
      required:
      - new_password1
      - new_password2
    CookieTokenRefresh:
      type: object
      properties:
        refresh:
          type: string
          description: WIll override cookie.
