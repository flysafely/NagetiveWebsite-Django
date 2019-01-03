function BlackListOperation(opreration,nickname,csrftoken){
  $.post('/BlackListOperation/',{'Operation':opreration,csrfmiddlewaretoken: csrftoken,'UserNick':nickname},function(status){
    if (status == 'login'){
      document.getElementById('loginbutton').click();
    }else{
      alert(status);
      location.reload();
    }
  })
}

function GetNotificationInfo(){
  var PushNotificationslist = document.getElementById('PushNotifications-list');
  if(PushNotificationslist){
    while(PushNotificationslist.hasChildNodes()){
      PushNotificationslist.removeChild(PushNotificationslist.firstChild);
    }
  }  
  $.get('/GetNotificationInfo/',{},function(returndata){
    if (returndata == 'login'){
      document.getElementById('loginbutton').click();  
    }else{
      var jsonData = JSON.parse(returndata)
      for (var i=0;i<jsonData.length;i++){
        var NTDiv = document.createElement('div');
        NTDiv.setAttribute('class', 'PushNotifications-item PushNotifications-newItem');
        NTDiv.setAttribute('style', 'font-size:14px;width:363px;background:#ffffff;border-bottom:1px solid  #EBEBEB;text-overflow:ellipsis; white-space:nowrap; overflow:hidden;');
        NTDiv.setAttribute('id', jsonData[i].NT_ID);

        var NTUser = document.createElement('a');
        NTUser.setAttribute('href', '/UserProfile?UserNickName='+ jsonData[i].NT_SourceUser +'&Select=Publish&PageNumber=1');
        NTUser.setAttribute('style', 'text-decoration:none;');
        NTUser.innerText = jsonData[i].NT_SourceUser + ' ';

        var NTDefualt = document.createElement('span');
        if (jsonData[i].NT_Sign == 'RollCallPublish'){
          NTDefualt.innerText = '  点您名了  ';
        }else{
          NTDefualt.innerText = '  回复了您  ';
        }
        
        var NTTopic = document.createElement('a');
        NTTopic.setAttribute('href', "javascript:RemoveNotificationInfo('one',"+ "'" +jsonData[i].NT_ID + "','/"+ jsonData[i].NT_URL +'?Part='+ jsonData[i].NT_Part +'&FilterWord='+ jsonData[i].NT_KeyID +"&PageNumber=" + jsonData[i].NT_PageNumber + "'," + "'" + jsonData[i].NT_AnchorID + "')");
        NTTopic.setAttribute('style', 'text-decoration:none;');
        NTTopic.setAttribute('title', jsonData[i].NT_Title);
        NTTopic.innerText = jsonData[i].NT_Title;

        NTDiv.appendChild(NTUser);
        NTDiv.appendChild(NTDefualt);
        NTDiv.appendChild(NTTopic);

        PushNotificationslist.appendChild(NTDiv);

      }
    }
  })
}

function RemoveNotificationInfo(method,ntid,url,anchorid){
  if (method == 'one'){
    window.location.href=url+'&Anchor='+anchorid;
    var NotificationCountNode = document.getElementById('NotificationCount');
    if (NotificationCountNode){
      NotificationCountNode.parentNode.removeChild(NotificationCountNode);
    }
    $.post('/RemoveNotificationInfo/',{'NT_ID':ntid});
    //highlightDiv = document.getElementById(anchorid);
    //highlightDiv.setAttribute('style', 'padding:18px 20px 18px 20px;margin-bottom:6px;border:2px solid  #FABCBA;');
  }else{
    var NT_ID_Array = [];
    var PushNotificationslist = document.getElementById('PushNotifications-list');
    while(PushNotificationslist.hasChildNodes()){
      if (PushNotificationslist.firstChild.getAttribute('id')){
        NT_ID_Array.push(PushNotificationslist.firstChild.getAttribute('id'));
        PushNotificationslist.removeChild(PushNotificationslist.firstChild);
      }else{
        PushNotificationslist.removeChild(PushNotificationslist.firstChild);
      }
    }
    NT_ID = NT_ID_Array.join(',');
    $.post('/RemoveNotificationInfo/',{'NT_ID':NT_ID});
    var NotificationCountNode = document.getElementById('NotificationCount');
    if (NotificationCountNode){
      NotificationCountNode.parentNode.removeChild(NotificationCountNode);
    }
    document.getElementById('PushNotificationsClose').click();
  }
}

function TickDiv(){
  var url = window.location.href;
  var AnchorIndex = url.indexOf("Anchor");
  if (AnchorIndex != -1) {
    var AnchorID = url.substring(AnchorIndex+7);
    document.getElementById(AnchorID).setAttribute('style', 'border:2px solid  #FABCBA;');
    window.scrollTo({top:document.getElementById(AnchorID).offsetTop,behavior:"smooth"});
  }
}

function CommentConversation(url,csrftoken,ObjectID,replayuser,replayeduser,from){
  $.post(url,{csrfmiddlewaretoken: csrftoken,'ObjectID':ObjectID,'replayuser':replayuser,'replayeduser':replayeduser,'from':from},function(status){})
}

function SpecialTopicFollow(url,csrftoken,SpecialTopicID){
  $.post(url,{csrfmiddlewaretoken: csrftoken,'SpecialTopicID':SpecialTopicID},function(status){
    if(status == 'follow'){
      alert('关注成功!');
      location.reload();
    }else if(status == 'login'){
      document.getElementById('loginbutton').click();      
    }else if(status == 'cancel'){
      alert('取消关注!');
      location.reload();
    }
  })  
}

function Circusee(url,FilterWord){
  $.get(url,{'RollCallID':FilterWord},function(status){
    if(status == 'collect'){
      alert('收藏成功!');
    }else if(status == 'login'){
      document.getElementById('loginbutton').click();      
    }else{
      alert(status);
    }
  })
}

function RollCallReplay(url,csrftoken,FilterWord){
  var RollCallReplayContent=document.getElementById('RollCallReplayTextArea').value;
  var Chk_RollCallReplayContent = RollCallReplayContent.replace(/(^s*)|(s*$)/g, "").length;
  if(Chk_RollCallReplayContent != 0){
    if(Chk_RollCallReplayContent < 10){
      alert('观点不能少于10个字符！')
    }else{
      if(Chk_RollCallReplayContent > 50){
        alert('观点不能多于50个字符!')
      }else{
        $.post(url,{csrfmiddlewaretoken: csrftoken,'RollCallReplayContent':RollCallReplayContent,'FilterWord':FilterWord},function(status){
          if(status=='replayok'){
            alert('回复成功！');
            location.reload();
          }else{
            alert(status);
          }           
        })
      }
    }
  }else{
    alert('请输入观点!')
  }
}

function RollCallPublish(url,csrftoken){
  var RollCallTitle = document.getElementById('RollCallTitle').value;
  var RollCallUserNick = document.getElementById('RollCallUserNick').value;
  var RollCallContent = document.getElementById('RollCallContent').value;
  var Chk_RollCallTitle = RollCallTitle.replace(/(^s*)|(s*$)/g, "").length;
  var Chk_RollCallUserNick = RollCallUserNick.replace(/(^s*)|(s*$)/g, "").length;
  var Chk_RollCallContent = RollCallContent.replace(/(^s*)|(s*$)/g, "").length; 
  if(Chk_RollCallTitle !=0 && Chk_RollCallUserNick !=0  &&  Chk_RollCallContent!=0){
    if(Chk_RollCallContent>30){
      alert('发表观点不能超过30个字符!');
    }else{
    $.post(url,{csrfmiddlewaretoken: csrftoken,'RollCallTitle':RollCallTitle,'RollCallUserNick':RollCallUserNick,'RollCallContent':RollCallContent},function(status){
      if(status=='publishok'){
        alert('发布成功！');
        location.reload();
      }else if(status=='login'){
        document.getElementById('EssayPublishBoardCancel').click();
        document.getElementById('loginbutton').click();
      }else if(status=='titleisexisted'){
        alert('点名标题内容已存在！');
      }else{
        alert(status);
      }      
    });}
  }else{
    alert('请完整输入必要栏目！');
  }
}

function Replay(url,csrftoken,commentid,from){
  var ArticleID = document.getElementById("ArticleBody").getAttribute('articleid');
  var CommentObject = document.getElementById('Replaybox#' + commentid);
  var Comment = CommentObject.value;
  var Chk_Comment = Comment.replace(/(^s*)|(s*$)/g, "").length;
  if(Chk_Comment!=0){
    $.post(url,{'From':from,csrfmiddlewaretoken: csrftoken,'ArticleID':ArticleID,'CommentID':commentid,'Comment':Comment},function(status){
      if(status=='replayok'){
        alert('回复成功！');
        location.reload();
      }else if(status=='login'){
        document.getElementById('loginbutton').click();
      }
    });    
  }else{
    alert('没有回复内容！');
    CommentObject.focus();
  }

}

function HideReplayBox(obj,id){
  obj.setAttribute('onclick', 'javascript:ShowReplayBox(this,'+ "'" + id + "'" +')');
  var idDIV = document.getElementById(id);
  if(idDIV){
    while(idDIV.hasChildNodes()){
      idDIV.removeChild(idDIV.firstChild);
    }
  }  
}

function ShowReplayBox(obj,id,csrftoken,from){
  obj.setAttribute('onclick', 'javascript:HideReplayBox(this,'+ "'" + id + "'" +')');

  var replayDiv = document.createElement('div');
  replayDiv.setAttribute('style', 'margin-top:8px;');
  var replaybox = document.createElement("textarea");
  replaybox.setAttribute('class', 'replaybox');
  replaybox.setAttribute('id', 'Replaybox#' + id);
  replayDiv.appendChild(replaybox);

  var replaybuttonDiv = document.createElement('div');
  replaybuttonDiv.setAttribute('style', 'margin-top:5px;')  
  var replaybutton = document.createElement("button");
  replaybutton.setAttribute('class', 'Button Button--primary Button--blue');
  replaybutton.innerText='确定';
  replaybutton.setAttribute('style', 'height:30px;width:60px;font-size:10px;margin-right:8px;')
  replaybutton.setAttribute('onclick', "javascript:Replay('/Replay/'," + "'" + csrftoken + "'" + "," + "'" + id + "'" + "," + "'" + from + "'" +")");
  var replaycancel = document.createElement("button");
  replaycancel.setAttribute('class', 'Button Button--primary');
  replaycancel.innerText='取消';
  replaycancel.setAttribute('style', 'height:30px;width:60px;font-size:10px;');
  replaycancel.setAttribute('onclick', 'javascript:HideReplayBox(this,'+ "'" + id + "'" +')');

  var parent = document.getElementById(id);
  replaybuttonDiv.appendChild(replaybutton);
  replaybuttonDiv.appendChild(replaycancel);
  replayDiv.appendChild(replaybuttonDiv);

  parent.appendChild(replayDiv);
}

function UserCollectCancel(obj,url,csrftoken){
  var ArticleID = obj.getAttribute("name");
  var TopicDIV = document.getElementById(ArticleID);
  if(TopicDIV){
      TopicDIV.parentNode.removeChild(TopicDIV);
  }
  $.post(url,{csrfmiddlewaretoken: csrftoken,'ArticleID':ArticleID},function(status){
                if(status=='collect'){
                  alert('已收藏');
                  location.reload();
                }else if(status=='cancel'){
                  alert('已取消收藏');
                  location.reload();
                }else{
                  document.getElementById('loginbutton').click();
                }
              });  
}

function UserCollect(url,csrftoken,ArticleID){
  var CollectButton = document.getElementById('CollectButton');
  CollectButton.disabled='disabled';
  $.post(url,{csrfmiddlewaretoken: csrftoken,'ArticleID':ArticleID
              },function(status){
                if(status=='collect'){
                  alert('已收藏');
                  location.reload();
                }else if(status=='cancel'){
                  alert('已取消收藏');
                  location.reload();
                }else{
                  document.getElementById('loginbutton').click();
                }
              }
        )
  setTimeout(function(){CollectButton.disabled='';},1000);
}

function UserLink(url,csrftoken,usernickname){
  var LinkButton = document.getElementById('LinkButton');
  LinkButton.disabled='disabled';
  $.post(url,{csrfmiddlewaretoken: csrftoken,
              'UserNickName':usernickname
              },function(status){
                if(status=='link'){
                  location.reload();
                  document.getElementById('LinkButton').innerText='取消关注';
                }else if(status=='cancel'){
                  location.reload();
                  document.getElementById('LinkButton').innerText='关注';
                }else if(status=='block'){
                  alert('对方已经将你拉黑！');
                }else if(status=='blockcancel'){
                  alert('取消拉黑！');
                  location.reload();
                }else{
                  document.getElementById('loginbutton').click();
                }
              }
        )
  setTimeout(function(){LinkButton.disabled='';},1000);
}

function UserProfileUpdate(url,csrftoken){
  var UserImageData = document.getElementById('UserImageChangeShow').src;
  var UserImageFormat = document.getElementById('UserImageChangeInput').value.split('.')[1];
  var UserNickName = document.getElementById('UserProfileNickName').value;
  var UserDescription = document.getElementById('UserProfileDescription').value;
  var UserSex = document.getElementById('UserProfileSexOptions').value;
  var UserConstellation = document.getElementById('UserProfileConstellation').value;
  var UserEmail = document.getElementById('UserProfileemail').value;
  var UserRegion = document.getElementById('UserProfileRegion').value;

  var Chk_UserNickName = UserNickName.replace(/(^s*)|(s*$)/g, "").length;
  var Chk_UserDescription = UserDescription.replace(/(^s*)|(s*$)/g, "").length;
  var Chk_UserSex = UserSex.replace(/(^s*)|(s*$)/g, "").length;
  var Chk_UserConstellation = UserConstellation.replace(/(^s*)|(s*$)/g, "").length;
  var Chk_UserEmail = UserEmail.replace(/(^s*)|(s*$)/g, "").length;
  var Chk_UserRegion = UserRegion.replace(/(^s*)|(s*$)/g, "").length;

  if(Chk_UserNickName !=0 && Chk_UserDescription !=0 && Chk_UserSex !=0 && Chk_UserConstellation !=0 && Chk_UserEmail !=0 && Chk_UserRegion !=0){
    $.post(url,{csrfmiddlewaretoken: csrftoken,
                'UserImageData':UserImageData,
                'UserImageFormat':UserImageFormat,
                'UserNickName':UserNickName,
                'UserDescription':UserDescription,
                'UserSex':UserSex,
                'UserConstellation':UserConstellation,
                'UserEmail':UserEmail,
                'UserRegion':UserRegion,
              },function(status){
                if(status=='Nick'){
                  alert('昵称已经存在!');
                }else {
                  window.location.href='/UserProfile?UserNickName=' + status + '&Select=Publish&PageNumber=1'
                  alert('修改成功!');
                }
              })

  }else{
    alert('必要信息不能为空！')
  }
}

function JumpToPage(mainurl,InputID,anchor){
  var PageNum = document.getElementById(InputID).value;
  window.location.href=mainurl+PageNum+'#'+anchor;
}


function QRcodeShare(URL){
  if(document.getElementById("QRcodeBoard").getAttribute('class')=='modal fade'){
    document.getElementById("qrcode").innerHTML = "";
  }
  var DomainName="http://www.nagetive.com"
  var qrcode = new QRCode(document.getElementById("qrcode"), {width : 200,height : 200});
  var elText = DomainName + URL;
  qrcode.makeCode(elText);
}

function clearQRcodeDivHtml(){
  document.getElementById("qrcode").innerHTML = "";
}

function StatisticTaste(Source,SpanID,ButtonID)
{
  var URL = '/StatisticTaste/';
  var ButtonElement = document.getElementById(ButtonID);
  var SpanElement = document.getElementById(SpanID);
  var ButtonName = ButtonID.split('#')[0];
  var ID = SpanID.split('#')[1];
  ButtonElement.disabled = 'disabled';
  if(ButtonName=='LikeButton'){
    ReverseButtonID =  'DislikeButton#' + ID;
    ReverseSpanID = 'DislikeSpan#' + ID;
    StandPoint = 'Like';
  }else{
    ReverseButtonID =  'LikeButton#' + ID;
    ReverseSpanID = 'LikeSpan#' + ID;
    StandPoint = 'Dislike';
  }
  ReverseButtonStatus = document.getElementById(ReverseButtonID).getAttribute('class')
  if (ButtonElement.getAttribute('class') == 'Button VoteButton VoteButton--up'){
    ButtonElement.setAttribute('class','Button VoteButton VoteButton--up is-active');
    document.getElementById(ReverseButtonID).setAttribute('class','Button VoteButton VoteButton--up');
    $.get(URL,{"Source":Source,"ID":ID,'StandPoint':StandPoint},function(status){
      if(status=='None'){
        if(StandPoint=='Like'){
          alert('你曾经赞过!');
        }else{
          alert('你曾经怼过!');
        }
      }else if(status=='login'){
        ClickButton('loginbutton');
      }else{
        SpanInt = parseInt(SpanElement.innerText) + 1;
        SpanElement.innerText = String(SpanInt);
        if(ReverseButtonStatus == 'Button VoteButton VoteButton--up is-active'){
          ReverseSpanInt = parseInt(document.getElementById(ReverseSpanID).innerText) - 1;
          document.getElementById(ReverseSpanID).innerText = String(ReverseSpanInt);
        }
      }
    });
  }else{
    ButtonElement.setAttribute('class','Button VoteButton VoteButton--up');
    $.get(URL,{"Source":Source,"ID":ID,'StandPoint':StandPoint + 'Cancel'},function(status){
      if(status=='login'){
        ClickButton('loginbutton');
      }else{
        SpanInt = parseInt(SpanElement.innerText) - 1;
        SpanElement.innerText = String(SpanInt);
      }
    });
  }
  setTimeout(function(){ButtonElement.disabled='';},1000);
}

function LongDissSubmit(url,csrftoken)
{   
    var Title = document.getElementById('LongArticleTitle').value;
    var Category = document.getElementById('categoryoptions');
    var CategoryID = Category.selectedIndex;
    var CategoryText = Category.options[CategoryID].text;
    var ContentRichText = CKEDITOR.instances.LongTextArea.getData();
    var ContentPoorText = CKEDITOR.instances.LongTextArea.document.getBody().getText().substring(0,140);

    var Themes = document.getElementById('LongArticleThemes').value;
    if(Title.replace(/(^s*)|(s*$)/g, "").length !=0 && ContentPoorText.replace(/(^s*)|(s*$)/g, "").length !=0 && Themes.replace(/(^s*)|(s*$)/g, "").length !=0){
      $.post(url,{csrfmiddlewaretoken: csrftoken,'Title':Title,'CategoryText':CategoryText,'ContentRichText':ContentRichText,'ContentPoorText':ContentPoorText,'Themes':Themes},function(status){
                                                                                                                                                if(status=='ok'){
                                                                                                                                                  alert('发布成功!');
                                                                                                                                                  location.reload();
                                                                                                                                                }else if(status=='login'){
                                                                                                                                                  alert('还未登录!');
                                                                                                                                                }else {
                                                                                                                                                  alert(status);
                                                                                                                                                }
    })
    }else{
      alert('请完整输入必要栏目!');
    }
    

}

function ClickButton(id)
{
    document.getElementById(id).click();
}

function CommentSubmit(url,csrftoken,from)
{   
    var TextAreaObject = document.getElementById("CommentTextArea");
    var TextAreaValue = TextAreaObject.value;
    var Chk_TextAreaValue = TextAreaValue.replace(/(^s*)|(s*$)/g, "").length;
    var ArticleID = document.getElementById("ArticleBody").getAttribute('articleid');
    if(Chk_TextAreaValue!=0){
      $.post(url, {'From':from,csrfmiddlewaretoken: csrftoken,'TextAreaValue':TextAreaValue,'ArticleID':ArticleID},function(status){if(status == 'ok'){alert('评论成功!');location.reload();}else{ClickButton('loginbutton');}});  
    }else{
      alert('没有输入评论内容!');
      TextAreaObject.focus();
    }
    
}

function LoginSubmit(url,csrftoken)
{   
    var username = document.getElementById('loginusername').value;
    var password = document.getElementById('loginpassword').value;
    $.post(url,{csrfmiddlewaretoken: csrftoken,'username':username,'password':password},function(status){if(status){alert('登录成功!');location.reload();}else{alert('用户名或密码错误！');}});
}

function Logout(url)
{
   $.get(url,function(status){
    if(status == 'Logout'){
      location.reload();
    }
   })
}

function RegistSubmit(url,csrftoken)
{
    var userimagedata = document.getElementById('UserImageShow').src;
    var format = document.getElementById('UserImageInput').value;
    var userimageformat = format.split('.')[1];
    var username = document.getElementById('registusername').value;
    var usernickname = document.getElementById('registusernickname').value;
    var password = document.getElementById('registpassword').value;
    var email = document.getElementById('registemail').value;
    $.post(url,{csrfmiddlewaretoken: csrftoken,'userimagedata':userimagedata,'userimageformat':userimageformat,'username':username,'usernickname':usernickname,'password':password,'email':email},function(status){if(status=='ok'){alert('注册成功!');location.reload();}else{alert(status);}});
}

function SearchTitle(source)
{
  var KeyWord = document.getElementById('searchinput').value;
  if(source == 'RollCall'){
    location.href='/RollCallSquare?Part=RollCallSearch&FilterWord='+KeyWord+'&PageNumber=1'; 
  }else if(source == 'SpecialTopic'){
    location.href='/SpecialTopicSquare?Part=SpecialTopicSearch&FilterWord='+KeyWord+'&PageNumber=1';
  }else {
    location.href='/Topics?Part=TopicSearch&FilterWord='+KeyWord+'&PageNumber=1'; 
  }

}

function CloseTopic(obj)
{
    
    var TopicID = obj.getAttribute("name");
    var TopicDIV = document.getElementById(TopicID);
    if(TopicDIV){
        TopicDIV.parentNode.removeChild(TopicDIV);
    }

}

function UploadImg(target,source)
{
    document.getElementById(target).setAttribute('data-source', source);
    document.getElementById(target).click()
}

function UploadUserImg(obj) {
  var file = obj.files[0];               
  console.log(obj);console.log(file);
  console.log("file.size = " + file.size);
  var reader = new FileReader();
  reader.onloadstart = function (e) {
     console.log("开始读取....");
  }
    reader.onprogress = function (e) {
         console.log("正在读取中....");
  }
  reader.onabort = function (e) {
     console.log("中断读取....");
  }
  reader.onerror = function (e) {
      console.log("读取异常....");
  }
  reader.onload = function (e) {
      console.log("成功读取....");
  var img = document.getElementById(obj.getAttribute('data-source'));
      img.src = e.target.result;
   //或者 img.src = this.result;  //e.target == this
  }
      reader.readAsDataURL(file)
  }
  function EssayPublish(){
    alert('发布')
  }