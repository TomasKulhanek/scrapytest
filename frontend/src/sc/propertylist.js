export class Propertylist {
    properties = [];

    attached() {
        fetch('http://localhost:8000/property')
            .then(response => response.json())
            .then(data => {
                this.properties = data;
                //console.log('properties',data);
            })
            .catch(error => console.error('Error fetching properties:', error));            
            //for debugging purposes
           //this.properties = [{"id":1,"title":"Prodej bytu 2+1 63 m² Finská, Kladno - Kročehlavy","image":"https://d18-a.sdn.cz/d_18/c_img_QQ_Ld/3E0BYyh.jpeg?fl=res,400,300,3|shr,,20|jpg,90","url":"https://www.sreality.cz/api/cs/v2/estates/4185273420"},{"id":2,"title":"Prodej bytu 2+kk 147 m² Libčice nad Vltavou, okres Praha-západ","image":"https://d18-a.sdn.cz/d_18/c_img_QN_J5/qhyBwqb.jpeg?fl=res,400,300,3|shr,,20|jpg,90","url":"https://www.sreality.cz/api/cs/v2/estates/461526092"},{"id":3,"title":"Prodej bytu 3+kk 184 m² Libčice nad Vltavou, okres Praha-západ","image":"https://d18-a.sdn.cz/d_18/c_img_QQ_Lg/VbM44d.jpeg?fl=res,400,300,3|shr,,20|jpg,90","url":"https://www.sreality.cz/api/cs/v2/estates/1687311436"},{"id":4,"title":"Prodej bytu 2+1 59 m² Lesní, Jablonec nad Nisou","image":"https://d18-a.sdn.cz/d_18/c_img_QR_MJ/2vmsig.jpeg?fl=res,400,300,3|shr,,20|jpg,90","url":"https://www.sreality.cz/api/cs/v2/estates/425583948"},{"id":5,"title":"Prodej bytu 3+1 67 m² 17. listopadu, Havířov - Podlesí","image":"https://d18-a.sdn.cz/d_18/c_img_QI_Jl/U6qBcMV.jpeg?fl=res,400,300,3|shr,,20|jpg,90","url":"https://www.sreality.cz/api/cs/v2/estates/3080037708"},{"id":6,"title":"Prodej bytu 3+kk 85 m² Dostalové, Praha 5 - Hlubočepy","image":"https://d18-a.sdn.cz/d_18/c_img_QI_Ji/tXhBlJn.jpeg?fl=res,400,300,3|shr,,20|jpg,90","url":"https://www.sreality.cz/api/cs/v2/estates/1874682956"}]
    }
}
