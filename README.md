# Chaos Kitty

Chaos Kitty is a Raspberry Pi-based project that interacts with AWS IoT Core to simulate changes in an AWS architecture based on a button press and visualizes the status with an LED stripe.

---

## **Setup**

### **Raspi Hardware Setup**
1. **Requirements**:
    - Raspberry Pi (or similar)
    - [LED stripe with Neopixels library support](https://www.adafruit.com/product/1138)

2. **Connections**:
    - [LED Stripe connected to Port 18](https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring)
    - [Button connected to Port 16](https://roboticsbackend.com/raspberry-pi-gpio-interrupts-tutorial/)

3. **Configuration**:
    - If you're planning to use different ports, make sure to modify `/src/utils/constants.py`:

        ```python
        BUTTON_PORT = 16
        NEOPIXEL_PORT = board.D18
        NEOPIXEL_NB_PIXELS = 100
        ```

### **Raspi Software Setup**
#### **1. Environment and Dependencies**
    
   - Verify if `virtualenv` is installed:
        ```bash
        python3 -m virtualenv --version
        ```
    
   - If not installed:
        ```bash
        python3 -m pip install virtualenv
        ```

   - Create a virtual environment:
        ```bash
        python3 -m virtualenv venv
        ```

   - Activate the virtual environment:
        ```bash
        source venv/bin/activate
        ```

   - Install necessary dependencies:
        ```bash
        pip install -r requirements.txt
        ```

#### **2. AWS IoT Core Setup**

   **TODO**: Include instructions on setting up AWS IoT Core for this setup.

   - Place your Raspberry Pi's AWS certificates in `src/utils/certificates`.
   - Update the parameters in `/src/utils/constants.py`.

### **Testing**

To test the setup:

1. Ensure the virtual environment is activated:
    ```bash
    source venv/bin/activate
    ```

2. Run the main script:
    ```bash
    python3 -m src.main
    ```

3. Test the integration by sending messages via the AWS IoT Core Test Broker on the topic `aws/bulb/<id>`, where `<id>` is between 31 and 38.

---

## **Understanding the Flow**

### 1. **User Action - Button Press**

The core interaction begins when a user presses the button connected to the Raspberry Pi:

- The button is linked to the Raspberry Pi on Port 16 (as defined in `/src/utils/constants.py`).
  
- When pressed, it triggers an event that leads to a message being published on a predefined MQTT topic. The topic and the message payload are determined by the following parameters in `/src/utils/constants.py`:

    ```python
    MQTT_CLIENT_PUBLISHING_TOPIC = "some/topic"
    MQTT_CLIENT_PUBLISHING_MESSAGE = "some-message"
    ```

### 2. **AWS Reaction to Published Message**

Upon receiving the message:

- The AWS infrastructure, particularly AWS IoT Core, detects the change and processes it. This results in alterations to specific components of your architecture.

- AWS IoT Core then broadcasts messages on various topics, like `aws/bulb/<id>`. Here, `<id>` is a numerical identifier ranging from 31 to 38, representing different components in your setup.

### 3. **LED Stripe Visualization**

The LED stripe connected to the Raspberry Pi acts as a visual indicator of the state of different AWS components:

- Each LED or a group of LEDs represents a specific component or service in your AWS architecture. 

- As messages are received on the `aws/bulb/<id>` topics, the LEDs change colors based on the message's payload:

    - `green`: Represents that the component/service is functioning normally or is compliant.
    - `red`: Indicates an issue or non-compliance with the component/service.

- The mapping between the `<id>` and the corresponding AWS service/component is defined in `/src/utils/constants.py`:

    ```python
    MQTT_ID_TO_STATE_MAPPING = { ... }
    ```

### 4. **Feedback Loop**

With the LEDs visualizing the status, users get immediate feedback on the AWS architecture's state post the button press. This can be useful for debugging, monitoring, or even gamifying the AWS setup.

---

## **Further Customization**

### 1. **Adapting MQTT Topics and Payloads**

If you wish to modify the MQTT topics your Raspberry Pi listens to or the expected payload messages:

- Head to `/src/utils/constants.py`:

    - Modify `MQTT_CLIENT_SUBSCRIPTION_TOPIC` for changing the topic.
    
    - Update `MQTT_CLIENT_SUBSCRIPTION_PAYLOAD_COMPLIANT` to adjust the expected compliant payload.

### 2. **Customizing Hardware Components**

To tailor the system to your specific AWS setup:

- Navigate to `src/main.py`. This file contains the logic that defines how your hardware (like the LEDs) reacts to different AWS component statuses.

- Here, you can add new components or modify existing ones by adjusting the `ArchitectureComponent` objects. An example:

    ```python
    example_architecture_component2 = architecture.ArchitectureComponent( ... )
    ```

- Components have various properties:

    - `neopixel_client`: This defines the interface with the LED strip.
    
    - `component_connections`: Represents connections within a component. 
    
    - `ingoing_connections`: Represents connections that are incoming to a component.
    
    - `outgoing_connections`: Represents connections going out from a component.

- If a component doesn't have certain connections, use an empty list: `component_connections=[]`.

- For multiple connections, use a list of `ConnectionComponent` objects.

### 3. **Configuring AWS Interactions**

Remember to keep the AWS IoT Core setup and Raspberry Pi in sync. If you modify the topics or payloads in the Raspberry Pi, ensure corresponding changes are made in AWS IoT Core's rules and actions.
