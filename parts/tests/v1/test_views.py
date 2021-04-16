from django.test import TestCase
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from parts.factories import PartFactory
from parts.models import Part
from parts.serializers import PartSerializer
from parts.v1.views import PartListView


class PartListViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.URL = reverse("parts:part-list")
        cls.client = APIClient()
        cls.expected_res = {
            "status_code": status.HTTP_200_OK,
            "count": 0,
            "res_len": 0,
            "next": None,
            "previous": None,
        }

    def test_sanitise_params(self):
        view = PartListView()
        # Case 1: No query param.
        # Expectation: Empty dict is returned.
        result = view._sanitise_params({})
        self.assertDictEqual(result, {})

        # Case 2: Invalid query params
        # Expectation: ValidationError is raised.
        params = {"make": "Ammann", "category": "ABC"}
        with self.assertRaises(ValidationError) as e:
            view._sanitise_params(params)
        self.assertEqual(
            str(e.exception.detail),
            (
                "[ErrorDetail(string='At lease one query param is invalid.', "
                "code='invalid')]"
            ),
        )

        # Case 3: Correct data without page_size and page.
        # Expectation: Dict with same data is returned.
        params = {"manufacturer": "Ammann", "category": "ABC"}
        result = view._sanitise_params(params)
        self.assertDictEqual(result, params)

        # Case 4: Correct data without page_size and page.
        # Expectation: Dict without the page and page_size keys is returned.
        new_params = {
            "manufacturer": "Ammann",
            "category": "ABC",
            "page": 1,
            "page_size": 10,
        }
        result = view._sanitise_params(new_params)
        self.assertDictEqual(result, params)

    def test_list(self):
        # Case 1: No data in the db.
        # Expectation: Empty list is returned.
        res = self.client.get(self.URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            dict(res.data), {"count": 0, "next": None, "previous": None, "results": []}
        )

        # Case 2: Data present and no params provided, data less than page size.
        # Expectation: All data is returned.
        no_of_instances = 5
        for _ in range(no_of_instances):
            PartFactory()
        res = self.client.get(self.URL)
        self.expected_res["count"] = self.expected_res["res_len"] = no_of_instances
        self._assert_response_data(res, filter_kwargs={})

        # Case 3:  Data present and one param is provided, data less than page size.
        # Expectation: Filtered data is returned.
        manufacturer1 = "Ammann"
        manufacturer2 = "Volvo"
        category = "Roller Parts"
        # Not using a loop to make sure that the category is not together.
        PartFactory(manufacturer=manufacturer1)
        PartFactory(manufacturer=manufacturer1, category=category)
        PartFactory(manufacturer=manufacturer1)
        PartFactory(manufacturer=manufacturer2, category=category)
        PartFactory(manufacturer=manufacturer1, category=category)
        PartFactory(manufacturer=manufacturer2)

        url = f"{self.URL}?manufacturer={manufacturer1}"
        res = self.client.get(url)
        self.expected_res["count"] = self.expected_res["res_len"] = 4
        filter_kwargs = {"manufacturer": manufacturer1}
        self._assert_response_data(res, filter_kwargs=filter_kwargs)

        # Case 3:  Data present and multiple params are provided,
        #          data less than page size.
        # Expectation: Filtered data is returned.
        url = f"{url}&category={category}"
        res = self.client.get(url)
        self.expected_res["count"] = self.expected_res["res_len"] = 2
        filter_kwargs["category"] = category
        self._assert_response_data(res, filter_kwargs=filter_kwargs)

    def _assert_response_data(self, res, filter_kwargs):
        """Helper method to run repeated assertions."""
        self.assertEqual(res.status_code, self.expected_res["status_code"])
        self._assert_pagination_data(res)

        q = Part.objects.filter(**filter_kwargs)
        data = PartSerializer(q, many=True).data
        self.assertListEqual(data, res.data["results"])

    def _assert_pagination_data(self, res):
        self.assertEqual(len(res.data["results"]), self.expected_res["res_len"])
        for key in ["count", "next", "previous"]:
            self.assertEqual(res.data[key], self.expected_res[key])

    def test_pagination(self):
        instance_count = 10
        for _ in range(instance_count):
            PartFactory()
        # Case 1: Data is less than default page size & page_size not provided.
        # Expectation: All data is returned. Both `previous` and `next` are null.
        res = self.client.get(self.URL)
        self.expected_res["count"] = self.expected_res["res_len"] = instance_count
        self._assert_pagination_data(res)

        # Case 2: `page_size` is less than data.
        # Expectation: Count of instances is equal to page_size.
        #              `previous` is null and `next` is populated.
        page_size = 3
        url = f"{self.URL}?page_size={page_size}"
        res = self.client.get(url)
        self.expected_res[
            "next"
        ] = f"http://testserver/api/v1/parts/?page=2&page_size={page_size}"
        self.expected_res["res_len"] = page_size
        self._assert_pagination_data(res)

        # Case 3: `page_size` is less than data, page is provided.
        # Expectation: Count of instances is equal to page_size.
        #              Both `previous` and `next` are populated.
        page = 2
        url = f"{url}&page={page}"
        res = self.client.get(url)
        self.expected_res[
            "next"
        ] = f"http://testserver/api/v1/parts/?page={page+1}&page_size={page_size}"
        self.expected_res[
            "previous"
        ] = f"http://testserver/api/v1/parts/?page_size={page_size}"
        self._assert_pagination_data(res)

        # Case 3: `page_size` is less than data, last page is fetched.
        # Expectation: Count of instances is equal to page_size.
        #              `previous` is populated and `next` is null.
        q, r = divmod(instance_count, page_size)
        page = q + 1 if r else q
        res_len = r if r else page_size
        prev_page = page - 1
        url = f"{url}&page={page}"
        res = self.client.get(url)
        self.expected_res["res_len"] = res_len
        self.expected_res["next"] = None
        self.expected_res[
            "previous"
        ] = f"http://testserver/api/v1/parts/?page={prev_page}&page_size={page_size}"
        self._assert_pagination_data(res)
