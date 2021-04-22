function reverse(array){
  console.log('Array in reverse order')
  for(var i=array.length-1;i>=0;i--){
    console.log(array[i])
  }
}

function identical(array){
  var first=array[0]
  for(var i=0;i<array.length;i++){
    if (array[i]!=first)
    {
      return false;
    }
  }
  return true;
}

function max(array){
  var first=array[0]
  for(var i=1;i<array.length;i++){
    if (array[i]>max)
    {
      max=array[i]
    }
  }
  return max
}

function sum(array){
  var sum=0
  for(num of array)
  {
    sum=sum+num
  }
  return num
}
