const baseApp = {
  delimiters: ["[[", "]]"],
  data() {
    return {
      sideBarIsVisible: false,
      currentBrandId: null,
      currentProductDetails: [],
      productLoadError: false,

      // Cart Products
      currentOrderList: [],

      // Form Values Start
      firstName: "",
      lastName: "",
      phoneNumber: "",
      GSTIN: "",
      password1: "",
      password2: "",
      landmark: "",
      town: "",
      district: "KN",
      pincode: "",
      phoneOTP: "",
      registerFormErrors: {
        firstName: "",
        lastName: "",
        GSTIN: "",
        password: "",
        landmark: "",
        town: "",
        district: "",
        pincode: "",
        phoneOTP: { message: "", status: null },
      },
      // Form Values End
      getOTPisLoading: false,
    };
  },
  mounted() {
    if (this.$refs["productsList"]) {
      // Get the default brand to be loaded when the app is loaded
      const defaultBrand = this.$refs["productsList"].dataset.defaultBrand;
      this.changeCurrentBrandId(parseInt(defaultBrand));
    } else if (this.$refs["cartList"]) {
      // Load the current user's unsubmitted order items (Fetch)
      const host = window.location.origin;
      const url = `${host}/api/orderlist`;
      // update the currentOrderList.
      fetch(url)
        .then((response) => {
          return response.json();
        })
        .then((response) => {
          this.currentOrderList.length = 0;
          for (item of response) {
            this.currentOrderList.push(item);
          }
        })
        .catch((err) => {
          console.log("Error while fetching data");
        });
    }
  },
  computed: {
    errorsInTheForm() {
      return !(
        this.firstName &&
        this.lastName &&
        this.phoneNumber &&
        this.phoneOTP &&
        this.password1 &&
        this.password2 &&
        this.landmark &&
        this.town &&
        this.district &&
        this.pincode &&
        !(
          this.registerFormErrors.firstName ||
          this.registerFormErrors.lastName ||
          this.registerFormErrors.GSTIN ||
          this.registerFormErrors.password ||
          this.registerFormErrors.landmark ||
          this.registerFormErrors.town ||
          this.registerFormErrors.district ||
          this.registerFormErrors.pincode ||
          !this.registerFormErrors.phoneOTP.status
        )
      );
    },
  },
  watch: {
    currentBrandId(value) {
      this.productLoadError = false;
      this.currentProductDetails = [];

      const host = window.location.origin;
      const url = `${host}/api/productlist/${value}`;
      fetch(url)
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          this.currentProductDetails = data;
        })
        .catch((data) => {
          this.productLoadError = true;
        });
    },
  },
  methods: {
    toggleSideBarVisiblity() {
      this.sideBarIsVisible = !this.sideBarIsVisible;
    },
    changeCurrentBrandId(value) {
      this.currentBrandId = value;
    },
    // Form Validation Methods
    firstNameCheck() {
      this.nameCheck(this.firstName, "firstName");
    },
    lastNameCheck() {
      this.nameCheck(this.lastName, "lastName");
    },
    nameCheck(value, errorField) {
      if (/^[a-zA-Z]+$/.test(value) && value.length <= 30) {
        this.registerFormErrors[errorField] = "";
      } else {
        this.registerFormErrors[errorField] = "Invalid Name";
      }
    },
    phoneNumberCheck() {
      if (/^[6-9]\d{9}$/.test(this.phoneNumber)) {
        this.registerFormErrors.phoneNumber = "";
      } else {
        this.registerFormErrors.phoneNumber = "Invalid Phone Number";
      }
    },
    phoneOTPCheck() {
      if (!this.phoneOTP) {
        this.registerFormErrors.phoneOTP.status = false;
        this.registerFormErrors.phoneOTP.message = "Please enter the OTP";
      } else {
        this.registerFormErrors.phoneOTP.status = true;
        this.registerFormErrors.phoneOTP.message = "";
      }
    },
    getOTP() {
      if (this.phoneNumber && !this.registerFormErrors.phoneNumber) {
        this.getOTPisLoading = true;
        const host = window.location.origin;
        const url = `${host}/user/sentOTP/`;
        const csrftoken = document.querySelector("#csrftoken input").value;
        fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({
            phoneNumber: this.phoneNumber,
          }),
        })
          .then((response) => {
            return response.json();
          })
          .then((data) => {
            if (data.status !== "pending") {
              throw "Unexpected Error";
            } else {
              this.registerFormErrors.phoneOTP.status = true;
              this.registerFormErrors.phoneOTP.message =
                "OTP sent! please check your phone";
            }
            this.getOTPisLoading = false;
          })
          .catch((error) => {
            this.registerFormErrors.phoneOTP.status = false;
            this.registerFormErrors.phoneOTP.message =
              "Couldn't send OTP, please try again later";
            this.getOTPisLoading = false;
          });
      } else {
        this.registerFormErrors.phoneOTP.status = false;
        this.registerFormErrors.phoneOTP.message =
          "Please enter a valid phone number!";
      }
    },
    GSTINCheck() {
      if (
        /\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}/.test(this.GSTIN)
      ) {
        this.registerFormErrors.GSTIN = "";
      } else if (!this.GSTIN) {
        this.registerFormErrors.GSTIN = "";
      } else {
        this.registerFormErrors.GSTIN = "Invalid GSTIN Number";
      }
    },
    passwordCheck() {
      this.registerFormErrors.password = "";
      const value = this.password1 || this.password2;
      if (value.length < 8) {
        this.registerFormErrors.password =
          "The Password Should Be Atleast 8 Characters Long";
        return;
      }
      if (this.password1 && this.password2) {
        if (this.password1 !== this.password2) {
          this.registerFormErrors.password = "The Passwords Do Not Match";
        }
      } else {
        this.registerFormErrors.password = "Both Password Fields Are Required";
      }
    },
    landmarkCheck() {
      if (!this.landmark) {
        this.isRequired("landmark");
      } else {
        this.isRequired("landmark", "clear");
      }
    },
    townCheck() {
      if (!this.town) {
        this.isRequired("town");
      } else {
        this.isRequired("town", "clear");
      }
    },
    isRequired(fieldName, clear = null) {
      if (clear) {
        this.registerFormErrors[fieldName] = "";
        return;
      }
      this.registerFormErrors[fieldName] = "This Field Is Required";
    },
    pincodeCheck() {
      if (!this.pincode) {
        this.isRequired("pincode");
        return;
      }
      if (this.pincode.length === 6 && !isNaN(this.pincode)) {
        this.registerFormErrors.pincode = "";
      } else {
        this.registerFormErrors.pincode = "Not A Valid Pincode";
      }
    },
    registrationCheck(event) {
      if (this.errorsInTheForm) {
        event.preventDefault();
      }
    },
    addViewToggle(event, product_id) {
      const queryTerm = "#product_" + product_id + " .cart-add-view";
      const elem = document.querySelector(queryTerm);
      elem.style.display == "none"
        ? (elem.style.display = "flex")
        : (elem.style.display = "none");
      event.target.innerText == "Cart"
        ? (event.target.innerText = "Done")
        : (event.target.innerText = "Cart");
    },
    redirectToLogin(next) {
      console.log(window.location);
      const origin = window.location.origin;
      window.location.href = origin + "/user/login/?next=/products";
    },
    addToCart(event, product_id) {
      const elem = event.target.parentNode.querySelector(".quantity-inp");
      const quantity = elem.value;
      // TODO add extra conditions like lower and upper limit in the below line
      if (/^\d+$/.test(quantity)) {
        const host = window.location.origin;
        const url = `${host}/api/orderproduct/`;
        const csrftoken = document.querySelector("#csrftoken input").value;
        fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({
            product_id: product_id,
            quantity: quantity,
          }),
        })
          .then((response) => {
            return response.json();
          })
          .then((value) => {
            // TODO Handle the response from the server on adding the product to cart
            console.log(value);
          })
          .catch((reason) => {
            console.log(reason);
          });

        // Close the add view after adding the product
        const queryTerm = "#product_" + product_id + " .cart-add-view";
        const elem = document.querySelector(queryTerm);
        elem.style.display = "none";
      } else {
        // Do Stuff
        // Make an error message *optional because the field is a number field
      }
    },
    showButton($event) {
      $event.target.parentNode.querySelector("button").style.display = "block";
    },
    updateOrderQuantity($event, orderid) {
      // FIXME This function can be used by anyone with an account to update anyone's orders
      const value = $event.target
        .closest(".cartitem")
        .querySelector(".quantity-inp").value;
      const host = window.location.origin;
      const url = `${host}/api/updateorder/`;
      const csrftoken = document.querySelector("#csrftoken input").value;
      fetch(url, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
          order_id: orderid,
          quantity: value,
        }),
      })
        .then((response) => {
          return response.json();
        })
        .then((response) => {
          // TODO On successful update of quantity of product, show something to the user
          if (response.status === true) {
            $event.target.closest("button").style.display = "none";
          }
        })
        .catch((reason) => {
          console.log(reason);
        });
    },
    deleteOrder(order_id) {
      // FIXME This function can be used by anyone with an account to delete anyone's orders
      const host = window.location.origin;
      const url = `${host}/api/deleteorder/`;
      const csrftoken = document.querySelector("#csrftoken input").value;
      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
          order_id,
        }),
      })
        .then((response) => {
          return response.json();
        })
        .then((response) => {
          // TODO Add an indication of the deletion in progress (as the request takes time to process)
          if (response.status === true) {
            const delOrderIndex = this.currentOrderList.findIndex(elem => elem.id === order_id);
            this.currentOrderList.splice(delOrderIndex, 1);
          }
        })
        .catch((reason) => {
          console.log(reason);
        });
    }
  },
};

Vue.createApp(baseApp).mount("body");

// TODO If debug==False, 1) Minify / Purge tailwindcss 2) Use Vuejs Production Version (minified) 3) Script JS - Minify 