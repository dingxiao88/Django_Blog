var tempGauge;
var client;

// mqtt服务基本要素
var target_ip;
var target_port;
var target_recv_topic;
var target_send_topic;

var msg_count;


function publish(topic, message) 
{
  message = new Paho.MQTT.Message(message);
  message.destinationName = topic;
  message.qos = 0;
  client.send(message);
}

function Send_Msg()
{
target_send_topic = $("#mqtt_send_tqp").val();

var msg =  $("#mqtt_send_msg").val();


publish(target_send_topic,msg);
//alert("ok"+Msg);

//@for py send pic
// client.publish('image', base64.b64encode(encimg), qos=0, retain=False)
}

function onConnect()
{
  target_recv_topic = $("#mqtt_recv_tqp").val();
  target_send_topic = $("#mqtt_send_tqp").val();

  if(target_recv_topic == target_send_topic)
  {
    this.subscribe( target_recv_topic );
  }
  else
  {
    this.subscribe( target_recv_topic );
    this.subscribe( target_send_topic );
  }
}

function Disconnect()
{
client.disconnect();
}

function Connect()
{
    // tempGauge = new steelseries.Radial('gaugeCanvas', {
    //   gaugeType: steelseries.GaugeType.TYPE4,
    //   minValue:-15,
    //   maxValue:50,
    //   size: 250,
    //   frameDesign: steelseries.FrameDesign.STEEL,
    //   knobStyle: steelseries.KnobStyle.STEEL,
    //   pointerType: steelseries.PointerType.TYPE6,
    //   lcdDecimals: 0,
    //   section: null,
    //   area: null,
    //   titleString: 'Temperature',
    //   unitString: 'C',
    //   threshold: 100,
    //   lcdVisible: true,
    //   lcdDecimals: 2
    //    });
    // tempGauge.setValue(''); //gives a blank display 'NaN' until broker has connected
    // tempGauge.setLedColor(steelseries.LedColor.RED_LED); //set the LED RED until connected


  target_ip = $("#mqtt_ip").val();
  target_port = parseInt($("#mqtt_port").val());
  target_recv_topic = $("#mqtt_recv_tqp").val();

  // alert(""+target_ip+target_port+target_topic)

  // 图片
  img = document.createElement( 'img' );
  img.width = "640";
  img.height = "480";
  img.src='';
  img.id = 'image_recv';
  container = document.getElementById( 'container' );
  container.appendChild( img );

  // 创建mqtt链接
  client = new Paho.MQTT.Client( target_ip, target_port, "clientId");

  client.onMessageArrived = function ( message )
  {

      var topic = message.destinationName;

      msg_count = msg_count + 1;

      // 显示接收到的信息
      if(topic != "pic")
      {
        // jquery方式赋值
        $("#mqtt_recv_msg").append(message.payloadString+'\n'); 
      }

      else if(topic == "pic")
      {
        if(target_recv_topic == "pic")
        {
          data = message.payloadBytes;
          img = document.getElementById( 'image_recv')
          img.src = 'data:image/png;base64,' +  btoa( String.fromCharCode.apply( null, data ) );
        }
      }
      // else if(topic == "dx")
      // {
      //   document.querySelector("#meter").value = message.payloadString; //更新显示
      //   tempGauge.setValue(message.payloadString);
      //   tempGauge.setLedColor(steelseries.LedColor.GREEN_LED); //change status LED to GREEN on broker connection
      // }

  }.bind( client );
  client.connect( { onSuccess: onConnect.bind( client ) } );
}
